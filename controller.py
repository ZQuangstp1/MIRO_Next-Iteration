import sys
import miro2 as miro 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ControllerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        
        # 1. Initialize Robot Interface
        try:
            self.interf = miro.lib.RobotInterface()
        except Exception as e:
            print(f"Warning: Could not connect to Robot Interface: {e}")
            self.interf = None
        
        # Movement parameters
        self.dtheta = 2.0  # Angular velocity (turning)
        self.dy = 0.2      # Linear velocity (forward/backward)
        self.timeout = 0.5 # Safety timeout for commands

        # 2. Continuous movement logic using QTimer
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.send_continuous_velocity)
        self.current_v = 0.0  # Target linear velocity
        self.current_w = 0.0  # Target angular velocity

        # 3. Setup User Interface
        self.initUI()

        # 4. Connect button events for press-and-hold functionality
        self.btn_up.pressed.connect(lambda: self.start_moving(self.dy, 0.0))
        self.btn_up.released.connect(self.stop_moving)
        
        self.btn_down.pressed.connect(lambda: self.start_moving(-self.dy, 0.0))
        self.btn_down.released.connect(self.stop_moving)
        
        self.btn_left.pressed.connect(lambda: self.start_moving(0.0, self.dtheta))
        self.btn_left.released.connect(self.stop_moving)
        
        self.btn_right.pressed.connect(lambda: self.start_moving(0.0, -self.dtheta))
        self.btn_right.released.connect(self.stop_moving)

        self.btn_stop.clicked.connect(self.stop_robot_emergency)

    def start_moving(self, v, w):
        """Sets the target velocities and starts the movement timer."""
        self.current_v = v
        self.current_w = w
        if not self.move_timer.isActive():
            self.move_timer.start(50) # Send command every 50ms for smooth motion

    def stop_moving(self):
        """Stops the timer and sends a zero-velocity command to the robot."""
        self.move_timer.stop()
        self.current_v = 0.0
        self.current_w = 0.0
        if self.interf:
            self.interf.set_vel(0, 0)

    def send_continuous_velocity(self):
        """Repeatedly called by the timer to maintain robot movement."""
        if self.interf:
            self.interf.set_vel(self.current_v, self.current_w, self.timeout)

    def stop_robot_emergency(self):
        """Immediate emergency halt."""
        self.stop_moving()
        print("Emergency Stop Triggered")

    def initUI(self):
        """Defines the layout and visual elements of the controller."""
        self.setWindowTitle("Navigate Miro")
        self.setFixedSize(360, 700)
        self.setStyleSheet("background-color: #F8FAFC;")
        
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

        # Forward Direction (Up)
        row_up = QHBoxLayout()
        self.btn_up = self.create_control_btn("↑")
        row_up.addStretch()
        row_up.addWidget(self.btn_up)
        row_up.addStretch()
        central_container.addLayout(row_up)

        # Steering (Left - Stop - Right)
        row_mid = QHBoxLayout()
        self.btn_left = self.create_control_btn("←")
        self.btn_stop = self.create_stop_btn() 
        self.btn_right = self.create_control_btn("→")
        row_mid.addWidget(self.btn_left)
        row_mid.addWidget(self.btn_stop)
        row_mid.addWidget(self.btn_right)
        central_container.addLayout(row_mid)

        # Backward Direction (Down)
        row_down = QHBoxLayout()
        self.btn_down = self.create_control_btn("↓")
        row_down.addStretch()
        row_down.addWidget(self.btn_down)
        row_down.addStretch()
        central_container.addLayout(row_down)

        window_layout.addLayout(central_container)
        window_layout.addStretch(1) 
        self.add_footer(window_layout)

    def create_control_btn(self, text):
        """Helper to create standardized navigation buttons."""
        btn = QPushButton(text)
        btn.setFixedSize(85, 85)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton { 
                background-color: white; 
                border-radius: 20px; 
                border: 1px solid #EEEEEE; 
                font-size: 32px; 
                color: #1A2B4C; 
            }
            QPushButton:pressed { 
                background-color: #F4F6F8; 
            }
        """)
        return btn

    def create_stop_btn(self):
        """Helper to create the emergency stop button."""
        btn = QPushButton("STOP")
        btn.setFixedSize(80, 80)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton { 
                background-color: #EF4444; 
                border-radius: 20px; 
                border: none; 
                color: white; 
                font-size: 16px; 
                font-weight: 900; 
            }
            QPushButton:pressed { 
                background-color: #DC2626; 
            }
        """)
        return btn

    def add_footer(self, parent_layout):
        """Adds status information at the bottom of the window."""
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
        if self.interf:
            self.interf.disconnect()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ControllerWindow()
    window.show()
    sys.exit(app.exec_())