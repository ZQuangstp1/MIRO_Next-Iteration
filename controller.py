import sys
import miro2 as miro # MiRo MDK Library
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ControllerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent # Reference to Main Menu
        self.setWindowTitle("Navigate Miro")
        self.setFixedSize(360, 700) 
        self.setStyleSheet("background-color: #F8FAFC;")
        
        # 1. Initialize Robot Interface from MDK
        # This connects directly to the local ROS nodes at UFV
        try:
            self.interf = miro.lib.RobotInterface()
        except Exception as e:
            print(f"Robot Interface not found: {e}")
            self.interf = None

        # 2. Movement parameters derived from client_manual.py
        self.dtheta = 2.0  # Rotation speed (angular)
        self.dy = 0.2      # Forward/Backward speed (linear)
        self.timeout = 0.5 # Safety timeout

        self.initUI()

    def initUI(self):
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)

        # --- HEADER SECTION ---
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(15, 20, 15, 10)

        back_btn = QPushButton("←")
        back_btn.setFixedSize(30, 30)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; font-size: 22px; font-weight: bold; color: #1A2B4C;")
        back_btn.clicked.connect(self.go_back)
        
        title_container = QVBoxLayout()
        title_label = QLabel("Navigate Miro")
        title_label.setStyleSheet("font-size: 22px; font-weight: 800; color: #1A2B4C; border:none;")
        subtitle_label = QLabel("Local MDK Control Mode")
        subtitle_label.setStyleSheet("font-size: 12px; color: #5E6C84; font-weight: 500; border:none;")
        title_container.addWidget(title_label)
        title_container.addWidget(subtitle_label)
        
        header_layout.addWidget(back_btn)
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        window_layout.addWidget(header_widget)

        # --- CENTRAL CONTROL AREA ---
        central_container = QVBoxLayout()
        central_container.setContentsMargins(20, 30, 20, 30)
        central_container.setSpacing(15) 

        # UP Row
        forward_layout = QHBoxLayout()
        self.btn_up = self.create_control_btn("↑")
        self.btn_up.mousePressEvent = lambda e: self.move_robot("up")
        forward_layout.addStretch()
        forward_layout.addWidget(self.btn_up)
        forward_layout.addStretch()
        central_container.addLayout(forward_layout)

        # MIDDLE Row (Left - Stop - Right)
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(15) 
        middle_layout.addStretch()

        self.btn_left = self.create_control_btn("←")
        self.btn_left.mousePressEvent = lambda e: self.move_robot("left")
        
        self.btn_stop = self.create_stop_btn() 
        self.btn_stop.mousePressEvent = lambda e: self.move_robot("stop")
        
        self.btn_right = self.create_control_btn("→")
        self.btn_right.mousePressEvent = lambda e: self.move_robot("right")

        middle_layout.addWidget(self.btn_left)
        middle_layout.addWidget(self.btn_stop)
        middle_layout.addWidget(self.btn_right)
        middle_layout.addStretch()
        central_container.addLayout(middle_layout)

        # DOWN Row
        backward_layout = QHBoxLayout()
        self.btn_down = self.create_control_btn("↓")
        self.btn_down.mousePressEvent = lambda e: self.move_robot("down")
        backward_layout.addStretch()
        backward_layout.addWidget(self.btn_down)
        backward_layout.addStretch()
        central_container.addLayout(backward_layout)

        window_layout.addLayout(central_container)
        window_layout.addStretch(1) 
        self.add_footer(window_layout)

    def move_robot(self, direction):
        """Processes movement logic directly through the Robot Interface."""
        linear = 0.0
        angular = 0.0

        if direction == "up":
            linear = self.dy
        elif direction == "down":
            linear = -self.dy
        elif direction == "left":
            angular = self.dtheta
        elif direction == "right":
            angular = -self.dtheta
        elif direction == "stop":
            linear = 0.0
            angular = 0.0

        # Execute command locally
        if self.interf:
            self.interf.set_vel(linear, angular, self.timeout)
            print(f"MDK Command: {direction} (Linear: {linear}, Angular: {angular})")
        else:
            print(f"No robot connected. Command ignored: {direction}")

    def create_control_btn(self, icon_text):
        frame = QFrame()
        frame.setFixedSize(85, 85)
        frame.setCursor(Qt.PointingHandCursor)
        frame.setStyleSheet("""
            QFrame { background-color: white; border-radius: 20px; border: 1px solid #EEEEEE; }
            QFrame:hover { background-color: #F4F6F8; }
        """)
        layout = QVBoxLayout(frame)
        label = QLabel(icon_text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 32px; font-weight: bold; color: #1A2B4C; border:none;")
        layout.addWidget(label)
        return frame

    def create_stop_btn(self):
        frame = QFrame()
        frame.setFixedSize(80, 80)
        frame.setCursor(Qt.PointingHandCursor)
        frame.setStyleSheet("""
            QFrame { background-color: #EF4444; border-radius: 20px; border: none; }
            QFrame:hover { background-color: #DC2626; }
        """)
        layout = QVBoxLayout(frame)
        label = QLabel("STOP")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; font-weight: 900; color: white; border:none;")
        layout.addWidget(label)
        return frame

    def add_footer(self, parent_layout):
        footer = QWidget()
        footer.setFixedHeight(80)
        footer.setStyleSheet("background-color: #F8FAFC; border-top: 1px solid #EEEEEE;")
        layout = QVBoxLayout(footer)
        
        status = QLabel("✅ Local MDK Connection Active")
        status.setAlignment(Qt.AlignCenter)
        status.setStyleSheet("color: #2E7D32; font-weight: 800; font-size: 12px; border:none;")
        
        info = QLabel("UFV Abbotsford Campus · Robot ID: RX-2025")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: #7A869A; font-size: 10px; border:none;")
        
        layout.addWidget(status)
        layout.addWidget(info)
        parent_layout.addWidget(footer)

    def go_back(self):
        if self.parent:
            self.parent.show()
            self.close()

    def closeEvent(self, event):
        """Ensure the robot interface is properly disconnected on exit."""
        if self.interf:
            self.interf.disconnect()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ControllerWindow()
    window.show()
    sys.exit(app.exec_())