import cv2
import rospy
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

class CameraWindow(QWidget):
    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu
        self.bridge = CvBridge()
        self.current_frame = None


        if not rospy.get_node_uri():
            rospy.init_node('gui_camera_node', anonymous=True)

        self.setWindowTitle("MiRo Eye Camera")
        self.setGeometry(200, 100, 480, 500)
        self.setStyleSheet("background-color: white;")

        self.sub_cam = rospy.Subscriber(
            "/miro/sensors/caml/compressed", 
            CompressedImage, 
            self.callback_camera
        )

        self.initUI()

        # --- 3. REFRESH TIMER ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33) 

    def callback_camera(self, ros_image):
        try:
            np_arr = np.frombuffer(ros_image.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if cv_image is not None:
                self.current_frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"ROS Callback Error: {e}")

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Back Button
        self.back_btn = QPushButton("← Back")
        self.back_btn.setFixedHeight(35)
        self.back_btn.setStyleSheet("font-weight: bold; color: #1A2B4C; border: none; text-align: left;")
        self.back_btn.clicked.connect(self.close_camera)

        # Camera Display Label
        self.label = QLabel("Waiting for camera data...")
        self.label.setFixedSize(440, 330) 
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background: black; color: white; border-radius: 12px;")

        layout.addWidget(self.back_btn)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def update_frame(self):
        """ Push the current_frame to the QLabel """
        if self.current_frame is not None:
            try:
                h, w, ch = self.current_frame.shape
                bytes_per_line = ch * w
                qt_img = QImage(self.current_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(qt_img).scaled(
                    self.label.width(), self.label.height(), Qt.KeepAspectRatio))
            except Exception as e:
                print(f"UI Refresh Error: {e}")

    def close_camera(self):
        self.timer.stop()
        self.sub_cam.unregister()
        if self.main_menu:
            self.main_menu.show()
        self.close()

    def closeEvent(self, event):
        self.close_camera()
        event.accept()