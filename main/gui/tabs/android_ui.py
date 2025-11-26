from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QProgressBar, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from gui.workers import AndroidWipeWorker, DeviceCheckWorker


class AndroidTab(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self._init_ui()

        # Poll for device connection automatically every 3 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_device_status)
        self.timer.start(3000)
        self.check_device_status()  # Initial check

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Card Frame
        card = QFrame()
        card.setObjectName("card")
        v_layout = QVBoxLayout(card)
        v_layout.setSpacing(15)

        # Header
        header = QLabel("Android Data Wiper")
        header.setObjectName("title")
        v_layout.addWidget(header)

        self.status_label = QLabel("Status: Scanning for devices...")
        self.status_label.setObjectName("subtitle")
        self.status_label.setStyleSheet("color: #ffd700;")  # Gold for waiting
        v_layout.addWidget(self.status_label)

        # Device Info Box
        self.info_frame = QFrame()
        self.info_frame.setStyleSheet("background: rgba(0,0,0,0.2); border-radius: 8px; padding: 10px;")
        info_layout = QHBoxLayout(self.info_frame)

        self.lbl_device_icon = QLabel("📱")
        self.lbl_device_icon.setStyleSheet("font-size: 32px; background: transparent;")
        info_layout.addWidget(self.lbl_device_icon)

        self.lbl_device_details = QLabel("No device connected")
        self.lbl_device_details.setStyleSheet("font-size: 14px; font-weight: bold; background: transparent;")
        info_layout.addWidget(self.lbl_device_details)
        info_layout.addStretch()

        v_layout.addWidget(self.info_frame)

        # Action Area
        action_row = QHBoxLayout()
        self.progress = QProgressBar()
        action_row.addWidget(self.progress)

        self.btn_wipe = QPushButton("INITIATE WIPE")
        self.btn_wipe.setObjectName("danger")
        self.btn_wipe.setEnabled(False)
        self.btn_wipe.clicked.connect(self.start_android_wipe)
        action_row.addWidget(self.btn_wipe)
        v_layout.addLayout(action_row)

        # Logs
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setPlaceholderText("ADB Logs will appear here...")
        v_layout.addWidget(self.log_box)

        layout.addWidget(card)

    def check_device_status(self):
        # Run check in background so UI doesn't stutter
        self.checker = DeviceCheckWorker()
        self.checker.result.connect(self._update_status_ui)
        self.checker.start()

    def _update_status_ui(self, status, device_id):
        if status == 'authorized':
            self.lbl_device_details.setText(f"Connected: {device_id}")
            self.status_label.setText("Status: Ready")
            self.status_label.setStyleSheet("color: #3bd67a;")  # Green
            if not self.worker:  # Only enable if not currently wiping
                self.btn_wipe.setEnabled(True)
        elif status == 'unauthorized':
            self.lbl_device_details.setText(f"Unauthorized: {device_id}")
            self.status_label.setText("Status: Please allow USB Debugging on phone")
            self.status_label.setStyleSheet("color: #ffb4b4;")  # Red
            self.btn_wipe.setEnabled(False)
        else:
            self.lbl_device_details.setText("No device detected")
            self.status_label.setText("Status: Waiting for USB connection...")
            self.status_label.setStyleSheet("color: #8b9bb4;")  # Grey
            self.btn_wipe.setEnabled(False)

    def _confirm_callback(self, model_name):
        return True

    def start_android_wipe(self):
        # Ask for confirmation HERE, on the main thread
        reply = QMessageBox.question(
            self,
            "Confirm Wipe",
            "Are you sure you want to wipe the connected Android device?\nThis cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.btn_wipe.setEnabled(False)
            self.log_box.clear()
            self.log_box.append("--- Starting Android Wipe Protocol ---")
            self.progress.setValue(0)

            # Pass a dummy callback that always returns True, since we already asked.
            self.worker = AndroidWipeWorker(confirmation_callback=lambda x: True)
            self.worker.signals.log.connect(self.log_box.append)
            self.worker.signals.progress.connect(self.progress.setValue)
            self.worker.signals.finished.connect(self._on_finished)
            self.worker.start()

    def _on_finished(self, success, msg):
        self.btn_wipe.setEnabled(True)
        self.progress.setValue(100)
        if success:
            QMessageBox.information(self, "Done", msg)
        else:
            QMessageBox.warning(self, "Result", msg)