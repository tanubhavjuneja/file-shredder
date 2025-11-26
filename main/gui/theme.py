# Shared Dark/Gradient Theme
STYLESHEET = """
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
    border: 1px solid rgba(255, 255, 255, 0.05);
}
/* Title Labels */
QLabel#title {
    font-size: 18px;
    font-weight: bold;
    color: #ffffff;
}
QLabel#subtitle {
    font-size: 12px;
    color: #8b9bb4;
}
/* Buttons */
QPushButton {
    background: qlineargradient(x1:0 y1:0, x2:0 y2:1,
        stop:0 #2a79ff, stop:1 #155edb);
    border: none;
    padding: 8px 12px;
    border-radius: 8px;
    font-weight: bold;
}
QPushButton:hover { background: #1f66e6; }
QPushButton:pressed { background: #104ba3; }
QPushButton:disabled { background: #3a4b60; color: #6c7b91; }

QPushButton#danger { 
    background: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #e63946, stop:1 #b91c1c);
}
QPushButton#danger:hover { background: #d32f2f; }

QPushButton#icon {
    background: transparent;
    font-size: 16px;
}

/* Inputs */
QLineEdit, QSpinBox, QTextEdit {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 6px;
    color: #e6eef8;
    selection-background-color: #2a79ff;
}
QLineEdit:focus, QSpinBox:focus {
    border: 1px solid #2a79ff;
}

/* --- SPINBOX BUTTONS (SVG Plus/Minus) --- */

QSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-top-right-radius: 8px;
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 1px;
}

QSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-bottom-right-radius: 8px;
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: 1px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background: #2a79ff;
}

QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {
    background: #155edb;
}

/* We use embedded SVG data URIs to render the symbols. 
   This avoids the 'square' artifact caused by CSS border hacks. */

/* PLUS SIGN (for Up) */
QSpinBox::up-arrow {
    width: 10px;
    height: 10px;
    image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path d='M4 0h2v10H4zM0 4h10v2H0z' fill='white'/></svg>");
}

/* MINUS SIGN (for Down) */
QSpinBox::down-arrow {
    width: 10px;
    height: 10px;
    image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path d='M0 4h10v2H0z' fill='white'/></svg>");
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: rgba(0,0,0,0.1);
    width: 8px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #3a4b60;
    min-height: 20px;
    border-radius: 4px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Progress Bar */
QProgressBar {
    background: rgba(255,255,255,0.04);
    border-radius: 8px;
    height: 18px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    border-radius: 8px;
    background: qlineargradient(x1:0 y1:0, x2:0 y2:1,
        stop:0 #3bd67a, stop:1 #16a34a);
}

/* Checkbox */
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
"""