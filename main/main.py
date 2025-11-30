"""
@fileoverview SuperShredder Application Entry Point

This module serves as the main entry point for the SuperShredder desktop application.
It creates a custom frameless PyQt6 window with a modern dark theme, featuring
sidebar navigation between Windows file shredding and Android device wiping modules.

Features:
    - Frameless window with custom title bar and drag support
    - Dark gradient theme with blue accents
    - Tabbed interface for Windows/Android operations
    - Custom window controls (minimize, close)

@author Team PD Lovers
@version 1.0.0
"""

import sys
import os
import ctypes
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from gui.theme import STYLESHEET
from gui.tabs.windows_ui import WindowsTab
from gui.tabs.android_ui import AndroidTab


def resource_path(relative_path: str) -> str:
    """
    Resolves the absolute path to a resource file.
    
    Handles both development environment and PyInstaller bundled executable.
    When running as a bundled .exe, PyInstaller extracts resources to a
    temporary folder stored in sys._MEIPASS.
    
    Args:
        relative_path: The relative path to the resource from the app root.
        
    Returns:
        The absolute path to the resource file.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    """
    Main application window for SuperShredder.
    
    Creates a frameless, draggable window with a custom dark theme.
    Features a sidebar for navigation between Windows and Android tabs,
    along with custom minimize and close controls.
    
    Attributes:
        btn_windows: Navigation button for Windows File Shredder tab.
        btn_android: Navigation button for Android Wiper tab.
        stack: QStackedWidget containing the tab content areas.
        windows_tab: The Windows file shredding interface.
        android_tab: The Android device wiping interface.
    """
    
    def __init__(self):
        """Initialize the main window with frameless styling and dark theme."""
        super().__init__()
        self.setWindowTitle("SuperShredder - Integrated")
        self.resize(900, 600)

        # Configure frameless window with translucent background
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(STYLESHEET + "\nQMainWindow { background: transparent; }")

        self.init_ui()
        self._drag_pos = None

    def init_ui(self):
        """
        Initialize the user interface components.
        
        Creates the main layout with:
        - Rounded container with gradient background
        - Left sidebar with navigation buttons and window controls
        - Right content area with stacked widget for tab switching
        """
        # Main container with rounded corners and gradient background
        container = QFrame()
        container.setObjectName("container")
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

        # Sidebar navigation panel
        sidebar = QFrame()
        sidebar.setStyleSheet(
            "background: rgba(0,0,0,0.3); border-top-left-radius: 20px; border-bottom-left-radius: 20px;")
        sidebar.setFixedWidth(200)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(10, 20, 10, 20)

        # Application title/logo
        title_lbl = QLabel("SUPER\nSHREDDER")
        title_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #2a79ff; padding-bottom: 20px;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side_layout.addWidget(title_lbl)

        # Navigation buttons for tab switching
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

        # Window control buttons (minimize, close)
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

        # Main content area with tab container
        content_area = QFrame()
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

    def switch_tab(self, index: int):
        """
        Switch between Windows and Android tabs.
        
        Updates the stacked widget index and applies active/inactive
        styling to the navigation buttons.
        
        Args:
            index: The tab index (0 for Windows, 1 for Android).
        """
        self.stack.setCurrentIndex(index)
        self.btn_windows.setChecked(index == 0)
        self.btn_android.setChecked(index == 1)

        active_style = "background: #2a79ff; color: white;"
        inactive_style = "background: transparent; color: #8b9bb4; text-align: left;"

        self.btn_windows.setStyleSheet(active_style if index == 0 else inactive_style)
        self.btn_android.setStyleSheet(active_style if index == 1 else inactive_style)

    def mousePressEvent(self, event):
        """
        Handle mouse press for window dragging.
        
        Records the initial position when left mouse button is pressed,
        enabling the frameless window to be dragged.
        
        Args:
            event: The mouse press event.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """
        Handle mouse move for window dragging.
        
        Moves the window to follow the cursor when dragging.
        
        Args:
            event: The mouse move event.
        """
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()


def main():
    """
    Application entry point.
    
    Initializes the Qt application, sets the Windows taskbar app ID
    for proper icon display, loads the window icon, and launches
    the main window.
    """
    # Set Windows AppUserModelID for proper taskbar icon grouping
    if sys.platform == 'win32':
        myappid = 'tarundeep.supershredder.gui.1.0'
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

    app = QApplication(sys.argv)

    # Load application icon
    icon_path = resource_path("icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Create and display main window
    window = MainWindow()
    window.switch_tab(0)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()