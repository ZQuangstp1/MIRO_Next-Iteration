# ===== COLOR SYSTEM =====
BG_MAIN = "#f8fafc"
PRIMARY = "#1A2B4C"
FONT = "#1A2B4C"
MUTED = "#F4F6F8"
BORDER = "#CCCCCC"
CARD_BG = "#FFFFFF"
ACCENT = "#cfe8f3"

# ===== GLOBAL STYLE =====
GLOBAL_STYLE = f"""
QWidget {{
    background-color: {BG_MAIN};
    color: {PRIMARY};
    font-family: Arial;
}}

QFrame {{
    background-color: {CARD_BG};
    border-radius: 15px;
    border: 1px solid {BORDER};
}}

QLineEdit {{
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 8px;
    background: white;
}}

QToolButton {{
    border: none;
    color: {FONT};
}}

QToolButton:hover {{
    color: {PRIMARY};
}}

QPushButton {{
    background: white;
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 6px;
}}

QPushButton:hover {{
    background: {ACCENT};
}}

QComboBox {{
    border: none;
    background: transparent;
}}

QSlider::groove:horizontal {{
    height: 6px;
    background: #E0E6ED;
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: {PRIMARY};
    width: 16px;
    border-radius: 8px;
}}
"""