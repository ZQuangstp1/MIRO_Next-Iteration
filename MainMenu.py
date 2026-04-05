import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import QSvgWidget
from settings import SettingsWindow
from camera import CameraWindow
from controller import ControllerWindow
from login import LoginWindow
from theme import *

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.settings_window = None
        self.setWindowTitle("Miro Smart Assistant")
        self.setGeometry(100, 100, 360, 640)
        self.setStyleSheet("background-color: white;")
        self.initUI()

    def initUI(self):
        main = QVBoxLayout()

        # ===== HEADER =====
        title = QLabel("Hey, Rigel!")
        title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {FONT};")

        subtitle = QLabel("What we’re doing today?")
        subtitle.setStyleSheet(f"font-size: 14px; color: {FONT};")

        header_layout = QHBoxLayout()

        # TEXT LEFT
        text_layout = QVBoxLayout()
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        logo = QSvgWidget("icons/Logo.svg")
        logo.setFixedSize(80, 80)

        # ADD
        header_layout.addLayout(text_layout)
        header_layout.addStretch()
        header_layout.addWidget(logo, alignment=Qt.AlignTop)

        main.addLayout(header_layout)
        # ===== SEARCH =====
        search = QLineEdit()
        search.setPlaceholderText("Search...")
        search.setFixedHeight(40)
        search.setStyleSheet("""
            QLineEdit {
                border: 2px solid black; 
                border-radius: 15px;
                background: white;
                padding-left: 10px;
                color: black;
            }
        """)
        main.addWidget(search)
        main.addSpacing(20)

        # ===== GRID CARDS =====
        grid = QGridLayout()
        grid.setSpacing(15)

        grid.addWidget(self.create_card("Open Camera", "icons/camera.svg"), 0, 0)
        grid.addWidget(self.create_card("Medication", "icons/med.svg"), 0, 1)
        grid.addWidget(self.create_card("Contact Services", "icons/contact.svg"), 1, 0)
        grid.addWidget(self.create_card("Navigate MIRO", "icons/robot.svg"), 1, 1)

        main.addLayout(grid)
        main.addStretch()

        # ===== BOTTOM MENU =====
        bottom = QFrame()
        bottom.setFixedHeight(80)
        bottom.setStyleSheet("""
            background-color: #cfe8f3;
            border-radius: 20px;
        """)


        bottom_layout = QHBoxLayout()

        bottom_layout.addWidget(self.create_nav("Home", "icons/home.svg"))
        bottom_layout.addWidget(self.create_nav("Setting", "icons/setting.svg"))
        bottom_layout.addWidget(self.create_nav("Profile", "icons/profile.svg"))

        bottom.setLayout(bottom_layout)
        main.addWidget(bottom)

        self.setLayout(main)

    # ===== CARD FUNCTION =====
    def create_card(self, text, icon_path):
        frame = QFrame()
        frame.setFixedSize(150, 150)
        frame.setObjectName("card")

        frame.setStyleSheet(f"""
            QFrame#card {{
                background-color: white;
                border-radius: 20px;
                border: 2px solid #CCCCCC;
            }}
            QFrame#card:hover {{
                background-color: #F4F6F8;
            }}
        """)

        layout = QVBoxLayout()

        icon = QLabel()
        pixmap = QPixmap(icon_path).scaled(
            60, 60,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation  
        )
        icon.setPixmap(pixmap)
        icon.setAlignment(Qt.AlignCenter)

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: black; font-size: 13px;")
        icon.setAttribute(Qt.WA_TransparentForMouseEvents)
        label.setAttribute(Qt.WA_TransparentForMouseEvents)

        icon.setStyleSheet("background: transparent;")
        label.setStyleSheet("background: transparent; color: black; font-size: 13px;")

        layout.addStretch()
        layout.addWidget(icon)
        layout.addWidget(label)
        layout.addStretch()

        frame.mousePressEvent = lambda event: self.handle_card_click(text)
        frame.setLayout(layout)
        return frame

    # ===== NAV BUTTON =====
    def create_nav(self, text, icon_path):
        btn = QToolButton()
        btn.setText(text)
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(24, 24))
        btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btn.setStyleSheet("""
            QToolButton {
                border: none;
                color: black;
            }
            QToolButton:hover {
                color: #0077b6;
            }
        """)

        btn.clicked.connect(lambda: self.handle_nav(text))
        return btn
    
   
    def handle_nav(self, text):
        if text == "Setting":
            if self.settings_window is None:
                self.settings_window = SettingsWindow(self)     
            self.settings_window.show()
            self.hide() 

    def handle_card_click(self, text):
        if text == "Open Camera":
            self.camera_window = CameraWindow(self)
            self.camera_window.show()
            self.hide()
        elif text == "Navigate MIRO": 
            self.controller_window = ControllerWindow(self)
            self.controller_window.show()
            self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    main_menu = App() # Create the main menu but don't show() it yet

    # Create login window and pass the main_menu.show function as the success callback
    login_screen = LoginWindow(on_success=main_menu.show)
    login_screen.show()

    sys.exit(app.exec_())
