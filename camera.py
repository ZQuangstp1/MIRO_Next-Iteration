import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from theme import *

class CameraWindow(QWidget):
    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu

        self.setWindowTitle("Camera")
        self.setGeometry(200, 100, 480, 500)
        self.setStyleSheet("background-color: white;")

        # ===== CAMERA INIT =====
        self.cap = cv2.VideoCapture(0)

        # ===== UI =====
        self.initUI()

        # ===== TIMER =====
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # ===== BACK BUTTON =====
        self.back_btn = QPushButton("← Back")
        self.back_btn.setFixedHeight(35)
        self.back_btn.setCursor(Qt.PointingHandCursor)

        self.back_btn.setStyleSheet("""
            QPushButton {
                border: NONE; 
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                color: #1A2B4C;
                text-align: left;
                padding-left: 5px;
            }
            QPushButton:hover {
                background-color: #F4F6F8;
            }
        """)

        self.back_btn.clicked.connect(self.close_camera)

        # ===== CAMERA VIEW =====
        self.label = QLabel()
        self.label.setFixedSize(440, 330) 
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(True)

        self.label.setStyleSheet("""
            background: black;
            border-radius: 12px;
        """)

        # ===== ADD =====
        layout.addWidget(self.back_btn)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

   
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        h, w, ch = frame.shape
        img = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)

        pix = QPixmap.fromImage(img)

        self.label.setPixmap(pix)

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        event.accept()

    def close_camera(self):
        # Stop camera safely
        self.timer.stop()
        self.cap.release()

        # Show main menu again
        self.main_menu.show()

        self.close()