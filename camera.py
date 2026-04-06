import cv2
import rospy
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from theme import *
import os

class CameraWindow(QWidget):
    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu
        self.bridge = CvBridge()
        self.setWindowTitle("MiRo Eye Camera")
        self.setGeometry(200, 100, 480, 500)
        self.setStyleSheet("background-color: white;")

     
        self.current_frame = None

        # ===== ROS SUBSCRIBER =====
       
        topic_base_name = "/" + os.getenv("MIRO_ROBOT_NAME", "miro")
        self.sub_cam = rospy.Subscriber(
            topic_base_name + "/sensors/caml/compressed", 
            CompressedImage, 
            self.callback_camera
        )

        # ===== UI =====
        self.initUI()

        # ===== TIMER =====
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def callback_camera(self, ros_image):
    
        try:
            self.current_frame = self.bridge.compressed_imgmsg_to_cv2(ros_image, "rgb8")
        except Exception as e:
            print(f"Error decoding image: {e}")

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
        self.label.setStyleSheet("background: black; border-radius: 12px;")

        layout.addWidget(self.back_btn)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def update_frame(self):
        if self.current_frame is not None:
            frame = self.current_frame
            h, w, ch = frame.shape
            img = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)
            self.label.setPixmap(pix)

    def closeEvent(self, event):
        self.timer.stop()
        self.sub_cam.unregister() 
        event.accept()

    def close_camera(self):
        self.timer.stop()
        self.sub_cam.unregister()
        self.main_menu.show()
        self.close()