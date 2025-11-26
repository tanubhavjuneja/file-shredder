import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QProgressBar, QSpinBox, QCheckBox,
    QFrame, QFileDialog, QMessageBox
)
from gui.workers import WindowsShredWorker


class WindowsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.targets = []
        self.worker = None
        self._init_ui()
        self.setAcceptDrops(True)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Card Frame
        card = QFrame()
        card.setObjectName("card")
        v_layout = QVBoxLayout(card)
        v_layout.setSpacing(15)

        # Header
        header = QLabel("Windows File Shredder")
        header.setObjectName("title")
        v_layout.addWidget(header)

        sub = QLabel("Select files or folders to permanently destroy using cryptographic algorithms.")
        sub.setObjectName("subtitle")
        v_layout.addWidget(sub)

        # Input Area
        input_row = QHBoxLayout()
        self.path_display = QLineEdit()
        self.path_display.setPlaceholderText("Drag files here or browse...")
        self.path_display.setReadOnly(True)
        input_row.addWidget(self.path_display)

        btn_file = QPushButton("Add File")
        btn_file.clicked.connect(lambda: self._browse(True))
        input_row.addWidget(btn_file)

        btn_folder = QPushButton("Add Folder")
        btn_folder.clicked.connect(lambda: self._browse(False))
        input_row.addWidget(btn_folder)
        v_layout.addLayout(input_row)

        # Options
        opts_row = QHBoxLayout()

        self.spin_passes = QSpinBox()
        # --- CHANGE START: Use Plus/Minus buttons instead of arrows ---
        self.spin_passes.setButtonSymbols(QSpinBox.ButtonSymbols.PlusMinus)
        # --- CHANGE END ---
        self.spin_passes.setPrefix("Passes: ")
        self.spin_passes.setRange(1, 35)
        self.spin_passes.setValue(3)
        opts_row.addWidget(self.spin_passes)

        self.cb_wipe_free = QCheckBox("Wipe Free Space")
        opts_row.addWidget(self.cb_wipe_free)
        opts_row.addStretch()
        v_layout.addLayout(opts_row)

        # Action Area
        action_row = QHBoxLayout()
        self.progress = QProgressBar()
        action_row.addWidget(self.progress)

        self.btn_start = QPushButton("SHRED FILES")
        self.btn_start.setObjectName("danger")
        self.btn_start.clicked.connect(self.start_shredding)
        action_row.addWidget(self.btn_start)
        v_layout.addLayout(action_row)

        # Logs
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        v_layout.addWidget(self.log_box)

        layout.addWidget(card)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path and os.path.exists(path):
                self.targets.append(path)
        self._update_display()

    def _browse(self, file_mode):
        if file_mode:
            path, _ = QFileDialog.getOpenFileName(self, "Select File")
        else:
            path = QFileDialog.getExistingDirectory(self, "Select Directory")

        if path:
            self.targets.append(path)
            self._update_display()

    def _update_display(self):
        self.path_display.setText("; ".join(self.targets))
        self.log_box.append(f"Queue updated: {len(self.targets)} targets.")

    def start_shredding(self):
        if not self.targets:
            QMessageBox.warning(self, "Error", "No targets selected.")
            return

        self.btn_start.setEnabled(False)
        self.progress.setValue(0)
        self.log_box.append("--- Starting Shred ---")

        self.worker = WindowsShredWorker(
            self.targets,
            self.spin_passes.value(),
            self.cb_wipe_free.isChecked(),
            chunk_size=1024 * 1024
        )
        self.worker.signals.log.connect(self.log_box.append)
        self.worker.signals.progress.connect(self.progress.setValue)
        self.worker.signals.finished.connect(self._on_finished)
        self.worker.start()

    def _on_finished(self, success, msg):
        self.btn_start.setEnabled(True)
        self.targets.clear()
        self._update_display()
        if success:
            QMessageBox.information(self, "Success", msg)
        else:
            QMessageBox.critical(self, "Error", msg)