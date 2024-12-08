from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QCheckBox, QGroupBox, QGridLayout, QTableWidgetItem
)
from PyQt5.QtCore import Qt, QTimer

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'python')))
# subthree modülünü import et
from acrome_embedded_devices import *

class ControlPage(QWidget):
    def __init__(self, stewart):
        super().__init__()
        self.stewart = stewart
        self.periodically_get_values = [Index_Stewart.Motor1_Position,
        Index_Stewart.Motor1_Position,
        Index_Stewart.Motor3_Position,
        Index_Stewart.Motor4_Position,
        Index_Stewart.Motor5_Position,
        Index_Stewart.Motor6_Position,
        Index_Stewart.PresentPosition_Roll,
        Index_Stewart.PresentPosition_Pitch,
        Index_Stewart.PresentPosition_Yaw]
        self.initUI()
        self.init_timer()

    def initUI(self):
        # Ana Layout
        main_layout = QHBoxLayout()

        # Sol taraf: Sliderlar ve Set butonu
        left_layout = QVBoxLayout()
        self.sliders = []
        self.slider_values = []

        self.slider_x = self.create_slider_layout('X axis', -200, 200, 0)
        self.slider_y = self.create_slider_layout('Y axis', -200, 200, 0)
        self.slider_z = self.create_slider_layout('Z axis', 500, 800, 500)
        self.slider_roll = self.create_slider_layout('Roll angle', -40, 40, 0)
        self.slider_pitch = self.create_slider_layout('Pitch angle', -40, 40, 0)
        self.slider_yaw = self.create_slider_layout('Yaw angle', -40, 40, 0)
        

        self.slider_x_layout = self.slider_x["layout"]
        self.slider_y_layout = self.slider_y["layout"]
        self.slider_z_layout = self.slider_z["layout"]
        self.slider_roll_layout = self.slider_roll["layout"]
        self.slider_pitch_layout = self.slider_pitch["layout"]
        self.slider_yaw_layout = self.slider_yaw["layout"]
        left_layout.addLayout(self.slider_x_layout)
        left_layout.addLayout(self.slider_y_layout)
        left_layout.addLayout(self.slider_z_layout)
        left_layout.addLayout(self.slider_roll_layout)
        left_layout.addLayout(self.slider_pitch_layout)
        left_layout.addLayout(self.slider_yaw_layout)

        # Set butonu
        set_button = QPushButton("Set")
        set_button.clicked.connect(self.on_set_button_clicked)  # Set butonu fonksiyonu
        left_layout.addWidget(set_button)

        # Sağ taraf: Enable toggle, Speed slider ve tablolar
        right_layout = QVBoxLayout()

        # Enable switch and speed slider
        speed_enable_layout = QHBoxLayout()

        # Enable Button (Toggle)
        self.enable_button = QPushButton("Enable")
        self.enable_button.setCheckable(True)  # Toggle için gerekli
        self.enable_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: 2px solid darkred;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:checked {
                background-color: green;
                border: 2px solid darkgreen;
            }
        """)
        self.enable_button.toggled.connect(self.toggle_enable)
        speed_enable_layout.addWidget(self.enable_button)

        # Speed slider
        speed_label = QLabel("Speed:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(10)
        self.speed_slider.setValue(5)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.valueChanged.connect(self.on_speed_slider_changed)  # Speed slider fonksiyonu

        speed_enable_layout.addWidget(speed_label)
        speed_enable_layout.addWidget(self.speed_slider)

        right_layout.addLayout(speed_enable_layout)

        # Motor pozisyon tablosu
        motor_pos_group_box = QGroupBox("Motor Positions")
        motor_table_layout = QVBoxLayout()
        self.motor_table = QTableWidget(1, 6)
        self.motor_table.setHorizontalHeaderLabels([f"Motor {i+1}" for i in range(6)])
        for i in range(6):
            self.motor_table.setColumnWidth(i, 80)
        motor_pos_group_box.setFixedSize(517, 115)

        motor_table_layout.addWidget(self.motor_table)
        motor_pos_group_box.setLayout(motor_table_layout)
        right_layout.addWidget(motor_pos_group_box)

        # IMU tablosu
        imu_group_box = QGroupBox("IMU Değerleri")
        imu_layout = QVBoxLayout()
        self.imu_table = QTableWidget(1, 3)
        self.imu_table.setHorizontalHeaderLabels(["Roll", "Pitch", "Yaw"])
        for i in range(3):
            self.imu_table.setColumnWidth(i, 100)
        imu_group_box.setFixedSize(337, 100)

        imu_layout.addWidget(self.imu_table)
        imu_group_box.setLayout(imu_layout)
        right_layout.addWidget(imu_group_box)

        # Sağ layout'u ortalama
        right_layout.setAlignment(Qt.AlignTop)

        # Ana layout'a alt layoutları ekleme
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Control Page")

    def create_slider_layout(self, label, min, max, initial):
        slider_layout = QHBoxLayout()
        slider_label = QLabel(label)
        slider_min_label = QLabel(str(min))
        slider_max_label = QLabel(str(max))

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setValue(initial)

        slider_value = QLineEdit(str(initial))
        slider_value.setFixedWidth(50)
        slider_value.setAlignment(Qt.AlignCenter)

        # Slider'ı ve LineEdit'i birbirine bağlama
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(slider_min_label)
        slider_layout.addWidget(slider)
        slider_layout.addWidget(slider_max_label)
        slider_layout.addWidget(slider_value)

        slider_layout_dict = {
            "label": slider_label,
            "layout": slider_layout,
            "slider_value": slider_value,
            "slider_min_label": slider_min_label,
            "slider_max_label": slider_max_label
        }

        slider.valueChanged.connect(lambda value, slider_val=slider_value: self.update_slider_value(slider_val, value))
        slider_value.editingFinished.connect(
            lambda _slider=slider, _slider_val=slider_value: self.update_slider_from_text(_slider, _slider_val)
        )

        return slider_layout_dict

    def init_timer(self):
        """QTimer'ı başlatır ve her 10 ms'de bir veri güncelleme fonksiyonunu çağırır."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tables)  # Timer ile bağlı fonksiyon
        self.timer.start(10)  # 10 ms aralıkla çalışır

    def update_slider_value(self, slider_value, value):
        slider_value.setText(str(value))

    def update_slider_from_text(self, slider, slider_val):
        try:
            value = int(slider_val.text())
            slider.setValue(value)
        except ValueError:
            slider_val.setText(str(slider.value()))

    def update_tables(self):
        """Motor ve IMU tablolarını günceller."""
        # Cihazdan motor pozisyonlarını al
        
        self.stewart.read_var(*self.periodically_get_values)
        motor_positions = [self.stewart._vars[i].value() for i in range(Index_Stewart.Motor1_Position, Index_Stewart.Motor6_Position)]
        imu_values = [ self.stewart._vars[i].value() for i in range(Index_Stewart.PresentPosition_Roll,Index_Stewart.PresentPosition_Yaw)]
        # write to the tables
        for i, position in enumerate(motor_positions):
            self.motor_table.setItem(0, i, QTableWidgetItem(f"{position:.2f}"))
        for i, imu in enumerate(imu_values):
            self.imu_table.setItem(0, i, QTableWidgetItem(f"{imu:.2f}"))

    def on_set_button_clicked(self):
        # Set button işlevi buraya eklenebilir
        x = float(self.slider_x["slider_value"].text())
        y = float(self.slider_y["slider_value"].text())
        z = float(self.slider_z["slider_value"].text())
        roll = float(self.slider_roll["slider_value"].text())
        pitch = float(self.slider_pitch["slider_value"].text())
        yaw = float(self.slider_yaw["slider_value"].text())
        print(x, y, z, roll, pitch, yaw)
        self.stewart.write_var([Index_Stewart.OperationMode, Stewart_ControlModes.InternalTrajectory])
        self.stewart.write_var([Index_Stewart.TargetCoordinate_X, x], [Index_Stewart.TargetCoordinate_Y, y], [Index_Stewart.TargetCoordinate_Z, z], [Index_Stewart.TargetRotation_Roll, roll], [Index_Stewart.TargetRotation_Pitch, pitch])


        print("Set button clicked!")

    def on_speed_slider_changed(self):
        # Speed slider işlevi buraya eklenebilir
        print(f"Speed slider value: {self.speed_slider.value()}")

    def toggle_enable(self,checked):
        # Enable switch işlevi buraya eklenebilir
        """Enable butonunun durumu değiştiğinde çağrılır."""
        if checked:
            self.stewart.write_var([Index_Stewart.TorqueEnable , 1])
            print("Enable ON")
        else:
            self.stewart.write_var([Index_Stewart.TorqueEnable , 0])
            print("Enable OFF")
