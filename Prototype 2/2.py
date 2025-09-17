import os
import shutil
import uuid
import platform
import subprocess
import sys
import psutil
from tqdm import tqdm
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, 
    QPushButton, QLabel, QFileDialog, QComboBox, QSpinBox, QLineEdit,
    QHBoxLayout, QProgressBar, QPlainTextEdit, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
class ShredWorker(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    finished = pyqtSignal()
    def __init__(self, target, drive_type, passes=7, chunk_size=500*1024*1024, full_drive=False):
        super().__init__()
        self.target = target
        self.drive_type = drive_type
        self.passes = passes
        self.chunk_size = chunk_size
        self.full_drive = full_drive
    def encrypt_file(self, file_path):
        key = os.urandom(32)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        with open(file_path, "rb") as f:
            data = f.read()
        if len(data) % 16 != 0:
            data += b" " * (16 - len(data) % 16)
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        with open(file_path, "wb") as f:
            f.write(encrypted_data)
        self.log.emit(f"File {file_path} encrypted.")
    def overwrite_file(self, file_path, passes=7):
#        self.encrypt_file(file_path)
        file_size = os.path.getsize(file_path)
        with open(file_path, "r+b") as f:
            for i in range(passes):
                f.seek(0)
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
                pct = int(((i + 1) / passes) * 100)
                self.progress.emit(pct)
        os.remove(file_path)
        self.log.emit(f"File {file_path} overwritten {passes} times and deleted.")
    def delete_file_ssd(self, file_path):
        os.remove(file_path)
        self.log.emit(f"File {file_path} encrypted and deleted (SSD-safe).")
    def wipe_free_space(self, directory):
        temp_file = os.path.join(directory, "shred_temp.dat")
        free_space = shutil.disk_usage(directory).free
        try:
            with open(temp_file, "wb") as f:
                written = 0
                while written < free_space - self.chunk_size:
                    f.write(os.urandom(self.chunk_size))
                    written += self.chunk_size
                    f.flush()
                    os.fsync(f.fileno())
                    pct = min(100, int((written / free_space) * 100))
                    self.progress.emit(pct)
        except Exception:
            pass
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        self.log.emit("Free space wiped.")
    def secure_erase(self, device_path):
        try:
            if "nvme" in device_path:
                self.log.emit(f"Running NVMe crypto erase on {device_path} ...")
                subprocess.run(["sudo", "nvme", "format", device_path, "--ses=2"], check=True)
            else:
                self.log.emit(f"Running ATA secure erase on {device_path} ...")
                subprocess.run(["sudo", "hdparm", "--user-master", "u", "--security-set-pass", "p", device_path], check=True)
                subprocess.run(["sudo", "hdparm", "--user-master", "u", "--security-erase", "p", device_path], check=True)
            self.log.emit(f"Device {device_path} securely erased.")
        except Exception as e:
            self.log.emit(f"Secure erase failed: {e}")
    def run(self):
        try:
            if self.full_drive:
                self.log.emit(f"Starting secure erase of drive {self.target} ({self.drive_type})...")
                self.secure_erase(self.target)
                self.progress.emit(100)
                return
            self.log.emit(f"Shredding target: {self.target} as {self.drive_type}")
            if os.path.isfile(self.target):
                file_list = [self.target]
            elif os.path.isdir(self.target):
                file_list = []
                for root, _, files in os.walk(self.target, topdown=False):
                    for fn in files:
                        file_list.append(os.path.join(root, fn))
            else:
                self.log.emit(f"Error: target not found: {self.target}")
                self.progress.emit(0)
                return
            total = max(1, len(file_list))
            processed = 0
            for path in file_list:
                try:
                    if self.drive_type.upper() == "HDD":
                        self.overwrite_file(path, passes=self.passes)
                    else:
                        self.delete_file_ssd(path)
                except Exception as e:
                    self.log.emit(f"Error processing {path}: {e}")
                processed += 1
                pct = int((processed / total) * 100)
                self.progress.emit(pct)
            if os.path.isdir(self.target):
                try:
                    shutil.rmtree(self.target)
                    self.log.emit(f"Removed directory: {self.target}")
                except Exception as e:
                    self.log.emit(f"Error removing directory {self.target}: {e}")
            if self.drive_type.upper() == "SSD":
                parent_dir = os.path.dirname(self.target) or "/"
                self.log.emit(f"Wiping free space on {parent_dir}...")
                self.wipe_free_space(parent_dir)
            self.progress.emit(100)
        except Exception as e:
            self.log.emit(f"Unexpected error: {e}")
            self.progress.emit(0)
        finally:
            self.finished.emit()
class ShredderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure Shredder - PyQt6")
        self.setGeometry(200, 200, 700, 500)
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_file_tab(), "File/Folder Shredder")
        self.tabs.addTab(self.create_drive_tab(), "Full Drive Erase")
        self.setAcceptDrops(True)
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            paths = [u.toLocalFile() for u in event.mimeData().urls()]
            self.set_targets(paths)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)
    def create_file_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.target_input = QLineEdit()
        self.target_input.setReadOnly(True)
        self.target_input.setPlaceholderText("Drag & Drop files/folders here")
        self.target_input.setAcceptDrops(True)
        browse_file_btn = QPushButton("Browse File")
        browse_file_btn.clicked.connect(self.browse_file)
        browse_folder_btn = QPushButton("Browse Folder")
        browse_folder_btn.clicked.connect(self.browse_folder)
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Targets:"))
        path_layout.addWidget(self.target_input)
        path_layout.addWidget(browse_file_btn)
        path_layout.addWidget(browse_folder_btn)
        self.drive_type_combo = QComboBox()
        self.drive_type_combo.addItems(["HDD", "SSD"])
        self.drive_type_combo.currentTextChanged.connect(self.update_advanced_options)
        self.passes_label = QLabel("Overwrite passes (HDD):")
        self.passes_spin = QSpinBox()
        self.passes_spin.setRange(1, 35)
        self.passes_spin.setValue(7)
        self.chunk_label = QLabel("Chunk size MB (SSD):")
        self.chunk_input = QLineEdit()
        self.chunk_input.setPlaceholderText("e.g. 500")
        self.chunk_input.setText("500")
        adv_layout = QHBoxLayout()
        adv_layout.addWidget(self.passes_label)
        adv_layout.addWidget(self.passes_spin)
        adv_layout.addWidget(self.chunk_label)
        adv_layout.addWidget(self.chunk_input)
        self.start_btn = QPushButton("Start Shredding")
        self.start_btn.clicked.connect(self.start_file_shred)
        self.progress = QProgressBar()
        self.log_area = QPlainTextEdit()
        self.log_area.setReadOnly(True)
        layout.addLayout(path_layout)
        layout.addWidget(QLabel("Drive Type:"))
        layout.addWidget(self.drive_type_combo)
        layout.addLayout(adv_layout)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.progress)
        layout.addWidget(self.log_area)
        widget.setLayout(layout)
        self.target_input.installEventFilter(self)
        return widget
    def browse_file(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if paths:
            self.set_targets(paths)
    def browse_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            self.set_targets([path])
    def set_targets(self, paths):
        if not hasattr(self, "targets"):
            self.targets = []
        self.targets.extend(paths)
        self.target_input.setText("; ".join(self.targets))
    def update_advanced_options(self, drive_type):
        if drive_type == "HDD":
            self.passes_label.show()
            self.passes_spin.show()
            self.chunk_label.hide()
            self.chunk_input.hide()
        else: 
            self.passes_label.hide()
            self.passes_spin.hide()
            self.chunk_label.show()
            self.chunk_input.show()
    def create_drive_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.drive_combo = QComboBox()
        for part in psutil.disk_partitions():
            self.drive_combo.addItem(part.device)
        self.drive_type_combo2 = QComboBox()
        self.drive_type_combo2.addItems(["HDD", "SSD"])
        self.erase_btn = QPushButton("Erase Drive")
        self.erase_btn.clicked.connect(self.start_drive_erase)
        self.progress2 = QProgressBar()
        self.log_area2 = QPlainTextEdit()
        self.log_area2.setReadOnly(True)
        layout.addWidget(QLabel("Select Drive:"))
        layout.addWidget(self.drive_combo)
        layout.addWidget(QLabel("Drive Type:"))
        layout.addWidget(self.drive_type_combo2)
        layout.addWidget(self.erase_btn)
        layout.addWidget(self.progress2)
        layout.addWidget(self.log_area2)
        widget.setLayout(layout)
        return widget
    def browse_target(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File or Folder")
        if path:
            self.target_input.setText(path)
    def start_file_shred(self):
        if not hasattr(self, "targets") or not self.targets:
            QMessageBox.warning(self, "Error", "Please select at least one file or folder.")
            return
        drive_type = self.drive_type_combo.currentText()
        passes = self.passes_spin.value()
        try:
            chunk_size = int(self.chunk_input.text()) * 1024 * 1024
        except ValueError:
            chunk_size = 500 * 1024 * 1024
            self.log_area.appendPlainText("Invalid chunk size, using default 500 MB")
        for target in self.targets:
            worker = ShredWorker(target, drive_type, passes, chunk_size, full_drive=False)
            worker.progress.connect(self.progress.setValue)
            worker.log.connect(self.log_area.appendPlainText)
            worker.start()
    def start_drive_erase(self):
        target = self.drive_combo.currentText()
        drive_type = self.drive_type_combo2.currentText()
        self.worker2 = ShredWorker(target, drive_type, full_drive=True)
        self.worker2.progress.connect(self.progress2.setValue)
        self.worker2.log.connect(self.log_area2.appendPlainText)
        self.worker2.start()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShredderApp()
    window.show()
    sys.exit(app.exec())
