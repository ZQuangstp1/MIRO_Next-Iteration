import sys
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import QSvgWidget # Required for .svg files

class LoginWindow(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success 
        self.setWindowTitle("MiRo Login")
        self.setFixedSize(360, 640)
        self.setStyleSheet("background-color: #F8FAFC;") # Light grey background
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(15)

        # 1. ADD LOGO (SVG) - Centered at the top
        self.logo = QSvgWidget("icons/Logo.svg")
        self.logo.setFixedSize(120, 120)
        
        logo_layout = QHBoxLayout()
        logo_layout.addStretch()
        logo_layout.addWidget(self.logo)
        logo_layout.addStretch()
        layout.addLayout(logo_layout)

        # 2. TITLE
        title = QLabel("Welcome Back")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #1A2B4C;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Sign in to your MiRo")
        subtitle.setStyleSheet("font-size: 13px; color: #5E6C84; margin-bottom: 20px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # 3. USERNAME INPUT (Fixed font color)
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setFixedSize(280, 50)
        self.username.setStyleSheet("""
            QLineEdit {
                padding: 10px; 
                border-radius: 12px; 
                border: 1px solid #E2E8F0; 
                background-color: white;
                color: #1A2B4C; 
                font-size: 14px;
            }
        """)

        # 4. PASSWORD INPUT (Hidden text + Fixed font color)
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password) # This hides the text (****)
        self.password.setFixedSize(280, 50)
        self.password.setStyleSheet("""
            QLineEdit {
                padding: 10px; 
                border-radius: 12px; 
                border: 1px solid #E2E8F0; 
                background-color: white;
                color: #1A2B4C; 
                font-size: 14px;
            }
        """)

        # 5. LOGIN BUTTON
        btn_login = QPushButton("Sign In")
        btn_login.setFixedSize(280, 55)
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #1A2B4C; 
                color: white; 
                border-radius: 12px; 
                font-weight: 800; 
                font-size: 16px;
                margin-top: 10px;
            }
            QPushButton:hover { background-color: #2D3E61; }
        """)
        btn_login.clicked.connect(self.handle_login)

        layout.addWidget(self.username, alignment=Qt.AlignCenter)
        layout.addWidget(self.password, alignment=Qt.AlignCenter)
        layout.addWidget(btn_login, alignment=Qt.AlignCenter)
        layout.addStretch()

    def handle_login(self):
        # Ensure your Node.js server is running on port 3000
        url = "https://miro-next-iteration.onrender.com/login"
        data = {"username": self.username.text(), "password": self.password.text()}
        
        try:
            response = requests.post(url, json=data, timeout=2)
            if response.status_code == 200:
                print("Login successful!")
                self.on_success() 
                self.close()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", "Could not connect to Auth Server.\nMake sure node auth_server.js is running.")