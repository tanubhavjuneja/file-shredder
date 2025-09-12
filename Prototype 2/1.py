import os
import sys
import psutil
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QCheckBox, QComboBox, QSpinBox, QMessageBox,
    QScrollArea, QProgressBar
)

# ---------------- Core Wipe Logic ----------------

class WipeMethod:
    ZERO = "Zeros"
    ONE = "Ones"
    RANDOM = "Random"


class WipeWorker(QThread):
    progress = pyqtSignal(int)       # emit % progress
    finished = pyqtSignal(str)       # emit result string

    def __init__(self, drive, chunk_mb, passes, method):
        super().__init__()
        self.drive = drive
        self.chunk_mb = chunk_mb
        self.passes = passes
        self.method = method

    def run(self):
        temp_path = os.path.join(self.drive, "wipe_temp.dat")
        chunk_size = self.chunk_mb * 1024 * 1024
        usage = psutil.disk_usage(self.drive)
        free_space = usage.free
        total_bytes = free_space * self.passes
        written = 0

        try:
            for p in range(self.passes):
                with open(temp_path, "wb") as f:
                    while written < total_bytes:
                        if self.method == WipeMethod.ZERO:
                            chunk = b"\x00" * chunk_size
                        elif self.method == WipeMethod.ONE:
                            chunk = b"\xFF" * chunk_size
                        else:
                            chunk = os.urandom(chunk_size)

                        try:
                            f.write(chunk)
                            written += len(chunk)
                        except OSError:
                            break  # disk full

                        # update progress
                        percent = int((written / total_bytes) * 100)
                        self.progress.emit(percent)

                try:
                    os.remove(temp_path)
                except FileNotFoundError:
                    pass

            self.finished.emit(f"✅ Wiped free space on {self.drive}")
        except Exception as e:
            self.finished.emit(f"❌ Error on {self.drive}: {e}")


# ---------------- GUI ----------------

class FreeSpaceWiperUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Free Space Wiper")
        self.resize(600, 500)
        self.drive_checkboxes = []
        self.progress_bars = {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select drives/partitions to wipe:"))

        # Scrollable area for drives
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        drive_container = QWidget()
        self.drive_layout = QVBoxLayout(drive_container)

        for part in psutil.disk_partitions(all=False):
            row = QHBoxLayout()
            chk = QCheckBox(f"{part.device} ({part.mountpoint}) - {part.fstype}")
            row.addWidget(chk)
            pb = QProgressBar()
            pb.setRange(0, 100)
            row.addWidget(pb)
            self.progress_bars[part.mountpoint] = pb
            self.drive_layout.addLayout(row)
            self.drive_checkboxes.append((chk, part.mountpoint))

        scroll.setWidget(drive_container)
        layout.addWidget(scroll)

        # Method selection
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("Overwrite Method:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems([WipeMethod.ZERO, WipeMethod.ONE, WipeMethod.RANDOM])
        method_layout.addWidget(self.method_combo)
        layout.addLayout(method_layout)

        # Chunk size
        chunk_layout = QHBoxLayout()
        chunk_layout.addWidget(QLabel("Chunk size (MB):"))
        self.chunk_spin = QSpinBox()
        self.chunk_spin.setRange(1, 2048)  # up to 2GB per chunk
        self.chunk_spin.setValue(512)
        chunk_layout.addWidget(self.chunk_spin)
        layout.addLayout(chunk_layout)

        # Passes
        passes_layout = QHBoxLayout()
        passes_layout.addWidget(QLabel("Overwrite passes:"))
        self.passes_spin = QSpinBox()
        self.passes_spin.setRange(1, 10)
        self.passes_spin.setValue(3)
        passes_layout.addWidget(self.passes_spin)
        layout.addLayout(passes_layout)

        # Wipe button
        wipe_btn = QPushButton("Start Wipe")
        wipe_btn.clicked.connect(self._on_start_wipe)
        layout.addWidget(wipe_btn)

        self.setLayout(layout)

    def _on_start_wipe(self):
        selected = [mount for chk, mount in self.drive_checkboxes if chk.isChecked()]
        if not selected:
            QMessageBox.warning(self, "No drive", "Please select at least one drive/partition.")
            return

        method = self.method_combo.currentText()
        chunk_size = self.chunk_spin.value()
        passes = self.passes_spin.value()

        for drive in selected:
            worker = WipeWorker(drive, chunk_mb=chunk_size, passes=passes, method=method)
            worker.progress.connect(self.progress_bars[drive].setValue)
            worker.finished.connect(self._on_wipe_finished)
            worker.start()

    def _on_wipe_finished(self, message: str):
        QMessageBox.information(self, "Wipe Completed", message)


# ---------------- Main ----------------

def main():
    app = QApplication(sys.argv)
    ui = FreeSpaceWiperUI()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
