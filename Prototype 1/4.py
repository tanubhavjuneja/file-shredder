import os
import sys
import uuid
import shutil
import random
import argparse
from pathlib import Path
from functools import partial
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QProgressBar,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QSpinBox, QCheckBox, QFrame
)
def encrypt_file_inplace(file_path: str):
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
def overwrite_file_once(path: str, chunk_size: int):
    size = os.path.getsize(path)
    with open(path, "wb") as f:
        remaining = size
        while remaining > 0:
            write_size = min(chunk_size, remaining)
            f.write(os.urandom(write_size))
            f.flush()
            os.fsync(f.fileno())
            remaining -= write_size
def secure_remove(path: str, passes: int, chunk_size: int):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    encrypt_file_inplace(path)
    file_size = os.path.getsize(path)
    for _ in range(passes):
        with open(path, "wb") as f:
            remaining = file_size
            while remaining > 0:
                write_size = min(chunk_size, remaining)
                f.write(os.urandom(write_size))
                f.flush()
                os.fsync(f.fileno())
                remaining -= write_size
    dir_name = os.path.dirname(path) or "."
    for _ in range(passes):
        random_name = os.path.join(dir_name, str(uuid.uuid4()))
        if os.path.exists(path):
            try:
                shutil.move(path, random_name)
                with open(random_name, "wb") as tf:
                    remaining = file_size
                    while remaining > 0:
                        write_size = min(chunk_size, remaining)
                        tf.write(os.urandom(write_size))
                        tf.flush()
                        os.fsync(tf.fileno())
                        remaining -= write_size
                os.remove(random_name)
            except FileNotFoundError:
                pass
def wipe_free_space(directory: str, chunk_size: int, writer_chunks=5):
    temp_file = os.path.join(directory, "shred_temp.dat")
    free_space = shutil.disk_usage(directory).free
    try:
        with open(temp_file, "wb") as f:
            for _ in range(writer_chunks):
                chunk = os.urandom(min(free_space, chunk_size))
                f.write(chunk)
                f.flush()
                os.fsync(f.fileno())
    except Exception:
        pass
    finally:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass
class ShredSignals(QObject):
    progress = pyqtSignal(int) 
    log = pyqtSignal(str) 
    finished = pyqtSignal(bool, str) 
    file_progress = pyqtSignal(str)
    canceled = pyqtSignal()
class ShredWorker(QThread):
    def __init__(self, target: str, passes: int, wipe_free: bool, chunk_size: int):
        super().__init__()
        self.signals = ShredSignals()
        self.target = target
        self.passes = passes
        self.wipe_free = wipe_free
        self.chunk_size = chunk_size
        self._stop_requested = False
    def request_stop(self):
        self._stop_requested = True
    def run(self):
        try:
            if not os.path.exists(self.target):
                self.signals.finished.emit(False, f"Target not found: {self.target}")
                return
            file_list = []
            if os.path.isdir(self.target):
                for root, _, files in os.walk(self.target, topdown=False):
                    for f in files:
                        file_list.append(os.path.join(root, f))
            else:
                file_list = [self.target]
            total_files = len(file_list)
            if total_files == 0:
                self.signals.finished.emit(False, "No files found to shred.")
                return
            self.signals.log.emit(f"Starting shredding: {self.target} ({total_files} file(s))")
            completed_files = 0
            for file_path in file_list:
                if self._stop_requested:
                    self.signals.log.emit("Operation cancelled by user.")
                    self.signals.canceled.emit()
                    self.signals.finished.emit(False, "Cancelled")
                    return
                self.signals.file_progress.emit(file_path)
                self.signals.log.emit(f"Processing: {file_path}")
                try:
                    secure_remove(file_path, self.passes, self.chunk_size)
                    self.signals.log.emit(f"Deleted {file_path}")
                except Exception as e:
                    self.signals.log.emit(f"Error on {file_path}: {e}")
                completed_files += 1
                percent = int((completed_files / total_files) * 80)
                self.signals.progress.emit(percent)
            if os.path.isdir(self.target):
                try:
                    shutil.rmtree(self.target)
                    self.signals.log.emit(f"Removed directory: {self.target}")
                except Exception as e:
                    self.signals.log.emit(f"Could not remove directory: {e}")
            if self.wipe_free:
                self.signals.log.emit("Starting free-space wipe (best-effort).")
                for i in range(5):
                    if self._stop_requested:
                        self.signals.log.emit("Operation cancelled during free-space wipe.")
                        self.signals.canceled.emit()
                        self.signals.finished.emit(False, "Cancelled")
                        return
                    try:
                        wipe_free_space(os.path.dirname(self.target) or ".", self.chunk_size)
                    except Exception as e:
                        self.signals.log.emit(f"Free-space wipe error: {e}")
                    self.signals.progress.emit(80 + int(((i + 1) / 5) * 20))
                self.signals.log.emit("Free-space wipe completed.")
            self.signals.progress.emit(100)
            self.signals.finished.emit(True, "Shredding completed successfully.")
        except Exception as e:
            self.signals.finished.emit(False, f"Unhandled error: {e}")
class ShredderUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Shredder")
        self.setMinimumSize(760, 420)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self._worker = None
        self._targets = []
        self.setAcceptDrops(True) 
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0 y1:0, x2:1 y2:1,
                    stop:0 #0f1724, stop:1 #071028);
                color: #e6eef8;
                font-family: "Segoe UI", Roboto, Arial;
                font-size: 12px;
            }
            QFrame#card {
                background: rgba(20, 28, 38, 230);
                border-radius: 14px;
                padding: 14px;
            }
            QPushButton {
                background: qlineargradient(x1:0 y1:0, x2:0 y2:1,
                    stop:0 #2a79ff, stop:1 #155edb);
                border: none;
                padding: 8px 12px;
                border-radius: 8px;
            }
            QPushButton:hover { background: #1f66e6; }
            QPushButton#cancel { background: #b23a3a; }
            QProgressBar {
                background: rgba(255,255,255,0.04);
                border-radius: 8px;
                height: 18px;
                text-align: center;
            }
            QProgressBar::chunk {
                border-radius: 8px;
                background: qlineargradient(x1:0 y1:0, x2:0 y2:1,
                    stop:0 #3bd67a, stop:1 #16a34a);
            }
            QTextEdit {
                background: rgba(255,255,255,0.02);
                border-radius: 8px;
            }
            QLineEdit, QSpinBox {
                background: rgba(255,255,255,0.03);
                border-radius: 8px;
                padding: 6px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 0px;
                height: 0px;
                border: none;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 1px solid #2a79ff;
                background: rgba(255,255,255,0.05);
            }
            QCheckBox::indicator:checked {
                background: #2a79ff;
                image: url(:/qt-project.org/styles/commonstyle/images/checkmark.png);
            }
        """)
        self._build_ui()
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        card = QFrame(self)
        card.setObjectName("card")
        v = QVBoxLayout(card)
        v.setSpacing(12)
        title_row = QHBoxLayout()
        title = QLabel("<b>File Shredder</b>")
        title.setStyleSheet("font-size:16px;")
        title_row.addWidget(title)
        title_row.addStretch()
        min_btn = QPushButton("—")
        min_btn.setFixedSize(34, 28)
        min_btn.clicked.connect(self.showMinimized)
        min_btn.setStyleSheet("background: transparent; color: #a9c1ff; font-weight: bold;")
        title_row.addWidget(min_btn)
        fs_btn = QPushButton("⬜")
        fs_btn.setFixedSize(34, 28)
        fs_btn.setCheckable(True)
        fs_btn.clicked.connect(lambda checked: self.showFullScreen() if checked else self.showNormal())
        fs_btn.setStyleSheet("background: transparent; color: #a9c1ff; font-weight: bold;")
        title_row.addWidget(fs_btn)
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(34, 28)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("background: transparent; color: #ffb4b4; font-weight: bold;")
        title_row.addWidget(close_btn)
        v.addLayout(title_row)
        input_row = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Select file or folder to shred... or drop them here")
        input_row.addWidget(self.path_edit)
        browse_file_btn = QPushButton("Browse File")
        browse_file_btn.clicked.connect(partial(self._on_browse, file_only=True))
        input_row.addWidget(browse_file_btn)
        browse_folder_btn = QPushButton("Browse Folder")
        browse_folder_btn.clicked.connect(partial(self._on_browse, file_only=False))
        input_row.addWidget(browse_folder_btn)
        v.addLayout(input_row)
        opts_row = QHBoxLayout()
        self.passes_spin = QSpinBox()
        self.passes_spin.setRange(1, 35)
        self.passes_spin.setValue(7)
        self.passes_spin.setPrefix("Passes: ")
        opts_row.addWidget(self.passes_spin)
        self.chunk_spin = QSpinBox()
        self.chunk_spin.setRange(1, 1024)  
        self.chunk_spin.setValue(100)   
        opts_row.addWidget(self.chunk_spin)
        chunk_label = QLabel("MB Chunk")
        opts_row.addWidget(chunk_label)
        self.wipe_cb = QCheckBox("Wipe free disk space")
        opts_row.addWidget(self.wipe_cb)
        opts_row.addStretch()
        v.addLayout(opts_row)
        pb_row = QHBoxLayout()
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        pb_row.addWidget(self.progress)
        self.start_btn = QPushButton("🚀 Start Shredding")
        self.start_btn.clicked.connect(self.start_shred)
        pb_row.addWidget(self.start_btn)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancel")
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_shred)
        pb_row.addWidget(self.cancel_btn)
        v.addLayout(pb_row)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(180)
        v.addWidget(self.log)
        root.addWidget(card)
        self._drag_pos = None
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.exists(path):
                self._targets.append(path)
                self._append_log(f"Added to queue: {path}")
        if self._targets:
            self.path_edit.setText("; ".join(self._targets))
    def start_shred(self):
        if not self._targets:
            target = self.path_edit.text().strip()
            if not target:
                QMessageBox.warning(self, "No target", "Please select or drop files/folders.")
                return
            self._targets = [target]
        if not all(os.path.exists(p) for p in self._targets):
            QMessageBox.warning(self, "Not found", "Some selected paths do not exist.")
            return
        passes = int(self.passes_spin.value())
        chunk_size = int(self.chunk_spin.value()) * 1024 * 1024
        wipe = self.wipe_cb.isChecked()
        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress.setValue(0)
        self._process_next(passes, wipe, chunk_size)
    def _process_next(self, passes, wipe, chunk_size):
        if not self._targets:
            self._append_log("Queue finished.")
            self.start_btn.setEnabled(True)
            self.cancel_btn.setEnabled(False)
            return
        target = self._targets.pop(0)
        self._append_log(f"Queued: {target} (passes={passes}, wipe_free={wipe}, chunk_size={chunk_size})")
        self._worker = ShredWorker(target=target, passes=passes, wipe_free=wipe, chunk_size=chunk_size)
        self._worker.signals.log.connect(self._append_log)
        self._worker.signals.progress.connect(self.progress.setValue)
        self._worker.signals.file_progress.connect(lambda f: self._append_log(f"Now: {f}"))
        self._worker.signals.finished.connect(lambda success, msg: self._on_finished(success, msg, passes, wipe, chunk_size))
        self._worker.signals.canceled.connect(lambda: self._append_log("Cancelled."))
        self._worker.start()
    def _on_finished(self, success, message, passes, wipe, chunk_size):
        self._append_log(f"Finished: {message}")
        if success:
            QMessageBox.information(self, "Done", message)
        else:
            QMessageBox.warning(self, "Stopped", message)
        self.progress.setValue(100 if success else self.progress.value())
        self._process_next(passes, wipe, chunk_size)
    def _append_log(self, text: str):
        self.log.append(text)
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())
    def cancel_shred(self):
        if self._worker:
            self._worker.request_stop()
            self._append_log("Cancel requested...")
    def _on_browse(self, file_only: bool):
        if file_only:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select file", os.path.expanduser("~"))
            if file_path:
                self._targets.append(file_path)
                self._append_log(f"Added to queue: {file_path}")
        else:
            folder = QFileDialog.getExistingDirectory(self, "Select folder", os.path.expanduser("~"))
            if folder:
                self._targets.append(folder)
                self._append_log(f"Added to queue: {folder}")
        if self._targets:
            self.path_edit.setText("; ".join(self._targets))
def run_cli():
    parser = argparse.ArgumentParser(description="Quantum-Secure File Shredder - CLI mode")
    parser.add_argument("target", help="Path to file or directory to shred")
    parser.add_argument("--passes", type=int, default=7, help="Overwrite passes (default 7)")
    parser.add_argument("--wipe-free-space", action="store_true", help="Wipe free disk space")
    args = parser.parse_args()
    target = args.target
    passes = args.passes
    wipe_free = args.wipe_free_space
    if not os.path.exists(target):
        print(f"Target not found: {target}")
        sys.exit(1)
    print(f"Shredding {target} (passes={passes}, wipe_free={wipe_free})")
    if os.path.isdir(target):
        files = []
        for root, _, filenames in os.walk(target, topdown=False):
            for fn in filenames:
                files.append(os.path.join(root, fn))
    else:
        files = [target]
    for idx, fpath in enumerate(files, 1):
        print(f"[{idx}/{len(files)}] {fpath}")
        try:
            secure_remove(fpath, passes)
        except Exception as e:
            print(f"Error shredding {fpath}: {e}")
    if os.path.isdir(target):
        try:
            shutil.rmtree(target)
        except Exception as e:
            print(f"Error removing directory: {e}")
    if wipe_free:
        print("Wiping free space (best-effort)...")
        wipe_free_space(os.path.dirname(target) or ".", writer_chunks=5)
    print("Done.")
def main():
    if len(sys.argv) > 1 and not (len(sys.argv) == 2 and sys.argv[1] == "--gui"):
        if "--gui" in sys.argv:
            pass
        else:
            run_cli()
            return
    app = QApplication(sys.argv)
    ui = ShredderUI()
    ui.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()