import sys
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import QSvgWidget
import pyrebase

firebase_config = {
    "apiKey": "AIzaSyD3vQ4VZpH1Qt5wMy6_Za_oM5OiUvG5DEk",
    "authDomain": "robot-asssistant.firebaseapp.com",
    "databaseURL": "https://robot-asssistant-default-rtdb.firebaseio.com",
    "projectId": "robot-asssistant",
    "storageBucket": "robot-asssistant.firebasestorage.app",
    "messagingSenderId": "730368792661",
    "appId": "1:730368792661:web:7fccc255c60c08acdd1cdc"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()


class LoginWindow(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success 
        self.setWindowTitle("MiRo Login")
        self.setFixedSize(360, 640)
        self.setStyleSheet("background-color: #F8FAFC;") 
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(15)

        # 1. ADD LOGO (SVG)
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

        # GOOGLE LOGIN BUTTON
        self.btn_google = QPushButton("Sign in with Google")
        self.btn_google.setFixedSize(280, 50)
        self.btn_google.setCursor(Qt.PointingHandCursor)
        self.btn_google.setStyleSheet("""
            QPushButton {
                background-color: white; 
                color: #1A2B4C; 
                border: 2px solid #1A2B4C;
                border-radius: 12px; 
                font-weight: bold;
                font-size: 14px;
                margin-top: 5px;
            }
            QPushButton:hover { background-color: #F0F4F8; }
        """)
        self.btn_google.clicked.connect(self.handle_google_login)
        layout.addWidget(self.btn_google, alignment=Qt.AlignCenter)
    def handle_login(self):
        email = self.username.text()
        password = self.password.text()

       
        popup_style = """
            QMessageBox {
                background-color: white;
                border: 2px solid #1A2B4C;
                border-radius: 10px;
            }
            QLabel {
                color: #1A2B4C;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #1A2B4C;
                color: white;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2D3E61;
            }
        """

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            raw_name = email.split('@')[0]
            display_name = raw_name.capitalize()
            # --- SUCCESS POPUP ---
            msg = QMessageBox(self)
            msg.setWindowTitle("Success")
            msg.setText("Login Successful!")
            msg.setInformativeText(f"Welcome back, {email}")
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet(popup_style) 
            msg.exec_()
            
            self.on_success(display_name)
            self.close()

        except Exception as e:
            # --- ERROR POPUP ---
            msg = QMessageBox(self)
            msg.setWindowTitle("Login Failed")
            msg.setText("Invalid Credentials")
            msg.setInformativeText("Please check your email and password.")
            msg.setIcon(QMessageBox.Critical)
            msg.setStyleSheet(popup_style)
            msg.exec_()

    def handle_google_login(self):
        import webbrowser

        popup_style = """
            QMessageBox {
                background-color: white;
                border: 2px solid #1A2B4C;
                border-radius: 10px;
            }
            QLabel {
                color: #1A2B4C;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #1A2B4C;
                color: white;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2D3E61;
            }
        """

        msg = QMessageBox(self)
        msg.setWindowTitle("Google Login")
        msg.setText("Redirecting to Browser...")
        msg.setInformativeText("Please complete the sign-in in your web browser.")
        msg.setStyleSheet(popup_style) 
        msg.exec_()
        
        # Open the Firebase Auth URL
        # Note: You would replace this with your actual Firebase Auth Domain link
        webbrowser.open(f"https://{firebase_config['authDomain']}/__/auth/handler")
     