import sys
import os
import ctypes  # <--- Added for Taskbar Icon Fix
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

# Import UI components
from gui.theme import STYLESHEET
from gui.tabs.windows_ui import WindowsTab
from gui.tabs.android_ui import AndroidTab


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SuperShredder - Integrated")
        self.resize(900, 600)

        # Remove default title bar for that custom hacker look
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Apply the global stylesheet
        # FIX 1: We specifically force the QMainWindow background to be transparent.
        self.setStyleSheet(STYLESHEET + "\nQMainWindow { background: transparent; }")

        self.init_ui()
        self._drag_pos = None

    def init_ui(self):
        # Main Container (Rounded, Dark)
        container = QFrame()
        container.setObjectName("container")
        # FIX 3: Moved the gradient to the container so the background respects the border radius.
        container.setStyleSheet("""
            QFrame#container {
                background: qlineargradient(x1:0 y1:0, x2:1 y2:1, stop:0 #0f1724, stop:1 #071028);
                border-radius: 20px;
                border: 1px solid #2a79ff;
            }
        """)
        self.setCentralWidget(container)

        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Sidebar ---
        sidebar = QFrame()
        sidebar.setStyleSheet(
            "background: rgba(0,0,0,0.3); border-top-left-radius: 20px; border-bottom-left-radius: 20px;")
        sidebar.setFixedWidth(200)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(10, 20, 10, 20)

        # App Title
        title_lbl = QLabel("SUPER\nSHREDDER")
        title_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #2a79ff; padding-bottom: 20px;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side_layout.addWidget(title_lbl)

        # Nav Buttons
        self.btn_windows = QPushButton("💾  File Shredder")
        self.btn_windows.setCheckable(True)
        self.btn_windows.setChecked(True)
        self.btn_windows.clicked.connect(lambda: self.switch_tab(0))
        side_layout.addWidget(self.btn_windows)

        self.btn_android = QPushButton("📱  Android Wiper")
        self.btn_android.setCheckable(True)
        self.btn_android.clicked.connect(lambda: self.switch_tab(1))
        side_layout.addWidget(self.btn_android)

        side_layout.addStretch()

        # Window Controls (Close/Min)

        # FIX 2: Added Minimize Button
        btn_min = QPushButton("Minimize")
        btn_min.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.05);
                color: #8b9bb4;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QPushButton:hover { background: rgba(255, 255, 255, 0.1); }
        """)
        btn_min.clicked.connect(self.showMinimized)
        side_layout.addWidget(btn_min)

        btn_close = QPushButton("Exit")
        btn_close.setObjectName("danger")
        btn_close.clicked.connect(self.close)
        side_layout.addWidget(btn_close)

        main_layout.addWidget(sidebar)

        # --- Content Area ---
        content_area = QFrame()
        # FIX 4: Explicitly style the content area to prevent square corners.
        content_area.setStyleSheet("""
            QFrame {
                background: transparent;
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }
            QStackedWidget, QStackedWidget > QWidget {
                background: transparent;
            }
        """)

        content_layout = QVBoxLayout(content_area)

        self.stack = QStackedWidget()
        self.windows_tab = WindowsTab()
        self.android_tab = AndroidTab()

        self.stack.addWidget(self.windows_tab)
        self.stack.addWidget(self.android_tab)

        content_layout.addWidget(self.stack)
        main_layout.addWidget(content_area)

    def switch_tab(self, index):
        self.stack.setCurrentIndex(index)
        # Update button states
        self.btn_windows.setChecked(index == 0)
        self.btn_android.setChecked(index == 1)

        active_style = "background: #2a79ff; color: white;"
        inactive_style = "background: transparent; color: #8b9bb4; text-align: left;"

        self.btn_windows.setStyleSheet(active_style if index == 0 else inactive_style)
        self.btn_android.setStyleSheet(active_style if index == 1 else inactive_style)

    # --- Dragging Logic for Frameless Window ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()


def main():
    # --- TASKBAR ICON FIX START ---
    # This block tells Windows that this is a unique application (AppUserModelID).
    # Without this, Windows groups it under a generic "Python" process and ignores your icon.
    if sys.platform == 'win32':
        myappid = 'tarundeep.supershredder.gui.1.0'  # Arbitrary unique string
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass
    # --- TASKBAR ICON FIX END ---

    app = QApplication(sys.argv)

    # Load and set the icon
    icon_path = resource_path("icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.switch_tab(0)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()