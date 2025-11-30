"""
@fileoverview Android Data Wiper Tab UI

Provides the user interface for Android device wiping functionality.
Automatically detects connected devices via ADB and allows users
to initiate factory reset or secure wipe operations.

Features:
    - Automatic device detection via ADB polling
    - Device status display (authorized, unauthorized, offline)
    - Confirmation dialog before wipe
    - Real-time progress and ADB log output

@author Team PD Lovers
@version 1.0.0
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QProgressBar, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from gui.workers import AndroidWipeWorker, DeviceCheckWorker


class AndroidTab(QWidget):
    """
    Android Data Wiper tab widget.
    
    Provides the complete UI for detecting Android devices,
    displaying device information, and initiating wipe operations.
    
    Attributes:
        worker: The background wipe worker thread.
        timer: QTimer for periodic device status polling.
        status_label: Label showing current connection status.
        lbl_device_details: Label showing connected device info.
        btn_wipe: Button to initiate the wipe operation.
        progress: Progress bar for operation status.
        log_box: Text area for ADB command logs.
    """
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self._init_ui()

        # Poll for device connection every 3 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_device_status)
        self.timer.start(3000)
        self.check_device_status()

    def _init_ui(self):
        """
        Initialize the tab's user interface components.
        
        Creates the layout with device status area, device info box,
        action buttons, progress bar, and log output.
        """
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
        """
        Start a background check for connected Android devices.
        
        Spawns a DeviceCheckWorker to poll ADB without blocking the UI.
        """
        self.checker = DeviceCheckWorker()
        self.checker.result.connect(self._update_status_ui)
        self.checker.start()

    def _update_status_ui(self, status: str, device_id: str):
        """
        Update the UI based on device connection status.
        
        Args:
            status: The device state ('authorized', 'unauthorized', etc.)
            device_id: The ADB device identifier.
        """
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
            self.status_label.setStyleSheet("color: #8b9bb4;")
            self.btn_wipe.setEnabled(False)

    def start_android_wipe(self):
        """
        Initiate the Android wipe operation after user confirmation.
        
        Shows a confirmation dialog and starts the wipe worker
        if the user confirms the action.
        """
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

            # Start wipe worker (confirmation already obtained)
            self.worker = AndroidWipeWorker(confirmation_callback=lambda x: True)
            self.worker.signals.log.connect(self.log_box.append)
            self.worker.signals.progress.connect(self.progress.setValue)
            self.worker.signals.finished.connect(self._on_finished)
            self.worker.start()

    def _on_finished(self, success: bool, msg: str):
        """
        Handle wipe operation completion.
        
        Re-enables the UI and shows a success or warning message.
        
        Args:
            success: Whether the operation completed successfully.
            msg: The completion message to display.
        """
        self.btn_wipe.setEnabled(True)
        self.progress.setValue(100)
        if success:
            QMessageBox.information(self, "Done", msg)
        else:
            QMessageBox.warning(self, "Result", msg)