import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ControllerWindow(QWidget):
    def __init__(self, main_menu=None):
        super().__init__()
        self.main_menu = main_menu
        self.setWindowTitle("Navigate Miro")
        self.setFixedSize(360, 700) 
        self.setStyleSheet("background-color: #F8FAFC;")
        self.initUI()

    def initUI(self):
        # Layout tổng của toàn bộ Window
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)

        # --- HEADER SECTION (Giống y hệt Settings) ---
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: #F8FAFC;")
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
        subtitle_label = QLabel("Manual Remote Control Mode")
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
        # 1. Row 1: FORWARD 
        forward_layout = QHBoxLayout()
  
        btn_up = self.create_control_btn("↑", 0.2, 0) 
        forward_layout.addStretch()
        forward_layout.addWidget(btn_up)
        forward_layout.addStretch()
        central_container.addLayout(forward_layout)

        # 2. Row 2: LEFT - STOP - RIGHT 
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(15) 
        middle_layout.addStretch()

        btn_left = self.create_control_btn("←", 0, 0.5)
        
        # STOP BUTTON 
        btn_stop = self.create_stop_btn() 
        
        btn_right = self.create_control_btn("→", 0, -0.5)

        middle_layout.addWidget(btn_left)
        middle_layout.addWidget(btn_stop)
        middle_layout.addWidget(btn_right)
        middle_layout.addStretch()
        central_container.addLayout(middle_layout)

        # 3. Row 3: BACKWARD
        backward_layout = QHBoxLayout()
        btn_down = self.create_control_btn("↓", -0.2, 0)
        backward_layout.addStretch()
        backward_layout.addWidget(btn_down)
        backward_layout.addStretch()
        central_container.addLayout(backward_layout)

        window_layout.addLayout(central_container)

        window_layout.addStretch(1) 
        self.add_footer(window_layout)

    def create_control_btn(self, icon_text, linear, angular):
        frame = QFrame()
        frame.setFixedSize(85, 85)
        frame.setCursor(Qt.PointingHandCursor)
        
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: 1px solid #EEEEEE;
            }
            QFrame:hover {
                background-color: #F4F6F8; 
            }
        """)

        layout = QVBoxLayout(frame)
        icon_lbl = QLabel(icon_text)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet("font-size: 32px; font-weight: bold; color: #1A2B4C; border:none; background:transparent;")
        layout.addWidget(icon_lbl)

        frame.mousePressEvent = lambda event: self.send_action(linear, angular)
        
        return frame

    def create_stop_btn(self):
        frame = QFrame()
        frame.setFixedSize(80, 80)
        frame.setCursor(Qt.PointingHandCursor)
        
        frame.setStyleSheet("""
            QFrame {
                background-color: #EF4444; 
                border-radius: 20px;
                border: none;
            }
            QFrame:hover {
                background-color: #DC2626;
            }
        """)
        
        v_layout = QVBoxLayout(frame)
        v_layout.setContentsMargins(10, 10, 10, 10)

        stop_lbl = QLabel("STOP")
        stop_lbl.setAlignment(Qt.AlignCenter)
        stop_lbl.setStyleSheet("font-size: 16px; font-weight: 900; color: white; border:none; background: transparent;")
        
        v_layout.addWidget(stop_lbl, alignment=Qt.AlignCenter)

        frame.mousePressEvent = lambda event: self.send_action(0, 0)
        return frame
        

    def add_footer(self, parent_layout):
        footer_widget = QWidget()
        footer_widget.setFixedHeight(80)
        footer_widget.setStyleSheet("background-color: #F8FAFC; border-top: 1px solid #EEEEEE;")
        footer_layout = QVBoxLayout(footer_widget)
        
        status = QLabel("✅ All systems operational")
        status.setAlignment(Qt.AlignCenter)
        status.setStyleSheet("color: #2E7D32; font-weight: 800; font-size: 12px; border:none;")
        
        info = QLabel("Robot ID: RX-2025-001 · Firmware v2.4.1")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: #7A869A; font-size: 10px; border:none;")
        
        footer_layout.addWidget(status)
        footer_layout.addWidget(info)
        parent_layout.addWidget(footer_widget)

    def send_action(self, linear, angular): 
        url = "https://next-iteration.onrender.com/robot/move"
        payload = {
            "token": "secure-session-token-001", 
            "linear": linear, 
            "angular": angular
        }
        print(f"Sending to Server: Linear={linear}, Angular={angular}")
        
        try:
            requests.post(url, json=payload, timeout=0.2)
        except Exception as e:
            print(f"Server error: {e}")

    def go_back(self):
        if self.main_menu:
            self.main_menu.show()
            self.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ControllerWindow()
    window.show()
    sys.exit(app.exec_())