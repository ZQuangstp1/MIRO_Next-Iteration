from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class SettingsWindow(QWidget):
    def __init__(self, main_menu=None):
        super().__init__()
        self.main_menu = main_menu
        self.setWindowTitle("Robot Settings")
        self.setFixedSize(360, 760) 
        self.initUI()

    def initUI(self):
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #F8FAFC;
                border: none;
            }
            QScrollBar:vertical {
                width: 0px;
                background: transparent;
            }
            QScrollBar:horizontal {
                height: 0px;
                background: transparent;
            }
        """)
        
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 
        
        container = QWidget()
        container.setStyleSheet("background-color: #F8FAFC;")

        scroll.setWidget(container)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(15, 20, 15, 20) 
        main_layout.setSpacing(15)

        # --- HEADER SECTION ---
        header_layout = QHBoxLayout()
        back_btn = QPushButton("←")
        back_btn.setFixedSize(30, 30)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("border: none; font-size: 22px; font-weight: bold; color: #1A2B4C;")
        
        if self.main_menu:
            back_btn.clicked.connect(self.go_back)
        
        title_container = QVBoxLayout()
        title_label = QLabel("Robot Settings")
        title_label.setStyleSheet("font-size: 22px; font-weight: 800; color: #1A2B4C; border:none;")
        subtitle_label = QLabel("Configure your robot preferences")
        subtitle_label.setStyleSheet("font-size: 12px; color: #5E6C84; font-weight: 500; border:none;")
        title_container.addWidget(title_label)
        title_container.addWidget(subtitle_label)
        
        header_layout.addWidget(back_btn)
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # --- BASIC INFO ---
        main_layout.addWidget(self.create_section_title("Basic Info"))
        main_layout.addWidget(self.create_editable_name_card("🤖  Atlas-X1"))

        time_layout = QHBoxLayout()
        time_layout.addWidget(self.create_time_card("🌞 Wake-up Time", "07:00 AM"))
        time_layout.addWidget(self.create_time_card("🌙 Sleep Time", "10:30 PM"))
        main_layout.addLayout(time_layout)

        # --- BATTERY & CHARGING ---
        main_layout.addWidget(self.create_section_title("Battery & Charging"))
        battery_card = QFrame()
        battery_card.setStyleSheet("background-color: #EBF7ED; border-radius: 18px; border: 1px solid #D0E7D2;")
        bat_v_layout = QVBoxLayout(battery_card)
        
        bat_header = QHBoxLayout()
        bat_label = QLabel("78%")
        bat_label.setStyleSheet("font-weight: 900; font-size: 18px; color: #1B5E20; border:none;")
        edit_btn = QPushButton("✎ Edit")
        edit_btn.setFixedSize(60, 25)
        edit_btn.setStyleSheet("background-color: white; border-radius: 8px; font-size: 10px; font-weight: bold; color: #1B5E20;")
        bat_header.addWidget(bat_label)
        bat_header.addStretch()
        bat_header.addWidget(edit_btn)
        bat_v_layout.addLayout(bat_header)

        progress = QProgressBar()
        progress.setValue(78)
        progress.setTextVisible(False)
        progress.setFixedHeight(12)
        progress.setStyleSheet("QProgressBar { background: #C8E6C9; border-radius: 6px; border:none; } QProgressBar::chunk { background: #2E7D32; border-radius: 6px; }")
        bat_v_layout.addWidget(progress)

        bat_footer = QHBoxLayout()
        charge_info = QLabel("Auto-Charge at 20%")
        charge_info.setStyleSheet("color: #1B5E20; font-size: 12px; font-weight: bold; border:none;")
        charge_btn = QPushButton("Charge")
        charge_btn.setFixedSize(75, 30)
        charge_btn.setStyleSheet("background-color: #1A2B4C; color: white; border-radius: 10px; font-weight: 900;")
        bat_footer.addWidget(charge_info)
        bat_footer.addStretch()
        bat_footer.addWidget(charge_btn)
        bat_v_layout.addLayout(bat_footer)
        
        main_layout.addWidget(battery_card)

      # --- ACTIVITY LEVEL ---
        main_layout.addWidget(self.create_section_title("Activity Level"))
        activity_frame = QFrame()
        activity_frame.setStyleSheet("background-color: white; border-radius: 18px; border: 1px solid #EEE;")
        act_layout = QHBoxLayout(activity_frame)
        act_layout.setContentsMargins(10, 10, 10, 10)

        self.activity_group = QButtonGroup(self)
        self.activity_buttons = []

        levels = ["Low", "Medium", "High"]
        for level in levels:
            btn = QPushButton(level)
            btn.setCheckable(True)
            btn.setFixedHeight(45)
            btn.setCursor(Qt.PointingHandCursor)
            
            btn.clicked.connect(self.update_activity_styles)
            
            self.activity_group.addButton(btn)
            self.activity_buttons.append(btn)
            act_layout.addWidget(btn)

        self.activity_buttons[1].setChecked(True)
        self.update_activity_styles()
        
        main_layout.addWidget(activity_frame)

      # --- SOUND SETTINGS SECTION ---
        main_layout.addWidget(self.create_section_title("Sound Settings"))
        
        sound_card = QFrame()
        sound_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 18px;
                border: 1px solid #EEEEEE;
            }
        """)
        
        sound_v_layout = QVBoxLayout(sound_card)
        sound_v_layout.setContentsMargins(15, 15, 15, 15)
        sound_v_layout.setSpacing(12)

        # 1. Volume Slider Row
        volume_layout = QHBoxLayout()
        vol_icon = QLabel("🔊")
        vol_icon.setStyleSheet("border: none; font-size: 14px;")
        
        slider = QSlider(Qt.Horizontal)
        slider.setValue(60)
        slider.setStyleSheet("""
            QSlider::groove:horizontal { height: 6px; background: #E0E6ED; border-radius: 3px; }
            QSlider::handle:horizontal {
                background: #1A2B4C; width: 18px; height: 18px;
                margin: -6px 0; border-radius: 9px;
            }
        """)
        volume_layout.addWidget(vol_icon)
        volume_layout.addWidget(slider)
        sound_v_layout.addLayout(volume_layout)

        voice_row = QFrame()
        voice_row.setStyleSheet("background-color: #F4F6F8; border-radius: 14px; border: none;")
        vr_layout = QHBoxLayout(voice_row)
        vr_layout.setContentsMargins(12, 8, 12, 8)

        voice_vbox = QVBoxLayout()
        voice_vbox.setSpacing(2)
        v_lbl = QLabel("Voice")
        v_lbl.setStyleSheet("color: #1A2B4C; font-weight: 800; font-size: 12px; border: none;")
        
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(["Aria (Female)","Luna (Female)", "Marcus (Male)", "Vincent (Male)"])
        self.voice_combo.setMinimumWidth(130) 
        self.voice_combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.voice_combo.view().setMinimumWidth(160)
        self.voice_combo.setStyleSheet(self.get_combobox_style())
        
        voice_vbox.addWidget(v_lbl)
        voice_vbox.addWidget(self.voice_combo)
        vr_layout.addLayout(voice_vbox)
        
        vr_layout.addStretch()

        pitch_layout = QHBoxLayout()
        self.pitch_combo = QComboBox()
        self.pitch_combo.addItems(["Normal", "High", "Low"])
        self.pitch_combo.setMinimumWidth(85)
        self.pitch_combo.view().setMinimumWidth(100) 
        self.pitch_combo.setStyleSheet(self.get_combobox_style(align_right=True))
        
        toggle = QCheckBox()
        toggle.setChecked(True)
        toggle.setStyleSheet("QCheckBox::indicator { width: 35px; height: 20px; }") # Thay bằng toggle custom nếu có

        pitch_layout.addWidget(self.pitch_combo)
        pitch_layout.addWidget(toggle)
        vr_layout.addLayout(pitch_layout)

        sound_v_layout.addWidget(voice_row)
        main_layout.addWidget(sound_card)

        window_layout.addWidget(scroll)
        
        self.add_footer(window_layout)

    def create_section_title(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("font-weight: 800; color: #1A2B4C; font-size: 14px; margin-top: 5px; border:none;")
        return lbl

    def create_time_card(self, title, default_time):
        frame = QFrame()
        frame.setStyleSheet("background: white; border-radius: 18px; border: 1px solid #EEE;")
        v_layout = QVBoxLayout(frame)
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("color: #1A2B4C; font-size: 11px; font-weight: 800; border:none;")
        
        time_row = QHBoxLayout()
        time_val = QLabel(default_time)
        time_val.setStyleSheet("font-weight: 900; font-size: 15px; color: #1A2B4C; border:none;")
        arrow = QLabel(">")
        arrow.setStyleSheet("color: #CCC; font-weight: bold; border:none;")
        time_row.addWidget(time_val)
        time_row.addStretch()
        time_row.addWidget(arrow)
        
        v_layout.addWidget(t_lbl)
        v_layout.addLayout(time_row)
        return frame

    def create_editable_name_card(self, default_name):
        frame = QFrame()
        frame.setFixedHeight(60)
        frame.setStyleSheet("background-color: white; border-radius: 18px; border: 1px solid #EEE;")
        layout = QHBoxLayout(frame)
        name_input = QLineEdit(default_name)
        name_input.setStyleSheet("border: none; font-size: 16px; font-weight: 900; color: #1A2B4C;")
        arrow = QLabel(">")
        arrow.setStyleSheet("color: #CCC; font-weight: bold; border:none;")
        layout.addWidget(name_input)
        layout.addStretch()
        layout.addWidget(arrow)
        return frame

    def add_footer(self, parent_layout):
        footer_widget = QWidget()
        footer_widget.setFixedHeight(80)
        footer_widget.setStyleSheet("background-color: #F8FAFC; border-top: 1px solid #EEE;")
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

    def get_combobox_style(self, align_right=False):
        alignment = "right" if align_right else "left"
        return f"""
            QComboBox {{
                border: none;
                background: transparent;
                color: #5E6C84;
                font-weight: bold;
                font-size: 13px;
                text-align: {alignment};
                padding: 2px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 15px;
            }}
            QComboBox::down-arrow {{
                image: none; 
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                border: 1px solid #DDD;
                border-radius: 8px;
                selection-background-color: #F0F2F5;
                selection-color: #1A2B4C;
                outline: none;
                padding: 5px;
            }}
        """
    def update_activity_styles(self):
        selected_style = """
            QPushButton {
                background-color: #1A2B4C;
                color: white;
                border-radius: 12px;
                font-weight: 800;
                border: none;
            }
        """
        default_style = """
            QPushButton {
                background-color: transparent;
                color: #5E6C84;
                font-weight: bold;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #F4F6F8;
            }
        """
        
        for btn in self.activity_buttons:
            if btn.isChecked():
                btn.setStyleSheet(selected_style)
            else:
                btn.setStyleSheet(default_style)

    def go_back(self):
        if self.main_menu:
            self.main_menu.show()
            self.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())