import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QCheckBox, QPushButton, QWidget, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

# src/python klasörünü sys.path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'python')))

# subthree modülünü import et
from acrome_embedded_devices import *

class PID_Table(QWidget):
    def __init__(self, stewart):
        super().__init__()
        self.stewart = stewart
        self.data = [[None for _ in range(7)] for _ in range(5)]  # 5 satır x 7 sütun veri saklama
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PID Table")
        self.setGeometry(200, 200, 600, 215)

        # Tablo oluştur
        self.table = QTableWidget(6, 7)  # 6 satır: 5 veri + 1 checkbox
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        self.table.setHorizontalHeaderLabels(["1", "2", "3", "4", "5", "6", "ALL"])
        self.table.setVerticalHeaderLabels(["P", "I", "D", "Gain", "Deadbend", ""])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Enable ALL Checkbox'ı ekle
        self.all_checkbox = QCheckBox("Enable ALL")
        self.all_checkbox.stateChanged.connect(self.toggle_all)
        self.table.setCellWidget(5, 6, self.all_checkbox)

        # Varsayılan düzenleme davranışı
        self.toggle_all(Qt.Unchecked)

        # Hücre değişimlerini yakala
        self.table.cellChanged.connect(self.cell_changed)

        # Set butonu ekle
        self.set_button = QPushButton("Set")
        self.set_button.clicked.connect(self.set_values)

        # Layout düzenle
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.set_button)
        self.setLayout(layout)

    def toggle_all(self, state):
        is_all_enabled = state == Qt.Checked

        for col in range(6):  # ALL dışındaki sütunlar
            for row in range(5):
                item = self.table.item(row, col)
                if not item:
                    item = QTableWidgetItem()
                    self.table.setItem(row, col, item)
                if is_all_enabled:
                    item.setFlags(Qt.NoItemFlags)  # Düzenleme kapalı
                    item.setBackground(QColor(200, 200, 200))  # Gri arka plan
                else:
                    item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)  # Düzenleme açık
                    item.setBackground(QColor(255, 255, 255))  # Beyaz arka plan

        for row in range(5):  # ALL sütunu
            item = self.table.item(row, 6)
            if not item:
                item = QTableWidgetItem()
                self.table.setItem(row, 6, item)
            if is_all_enabled:
                item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)  # Düzenleme açık
                item.setBackground(QColor(255, 255, 255))  # Beyaz arka plan
            else:
                item.setFlags(Qt.NoItemFlags)  # Düzenleme kapalı
                item.setBackground(QColor(200, 200, 200))  # Gri arka plan

    def cell_changed(self, row, col):
        # ALL sütunundaki bir hücre değiştirildiğinde diğer sütunlara kopyala
        if col == 6 and self.all_checkbox.isChecked():
            all_value = self.table.item(row, col).text()
            for target_col in range(6):  # 1, 2, 3, 4, 5, 6 sütunlarına kopyala
                self.table.item(row, target_col).setText(all_value)

        # Tablo verilerini güncelle
        self.update_data()

    def update_data(self):
        # Tablo verilerini `self.data` içine kaydet
        for row in range(5):
            for col in range(7):
                item = self.table.item(row, col)
                self.data[row][col] = item.text() if item else None

    def upload_data(self):
        pid_table_list = [[],[],[],[],[]]
        for i in range(Index_Stewart.Motor1_P, Index_Stewart.Motor6_P + 1):
            pid_table_list[0].append(self.stewart._vars[i].value())
        for i in range(Index_Stewart.Motor1_I, Index_Stewart.Motor6_I + 1):
            pid_table_list[1].append(self.stewart._vars[i].value())
        for i in range(Index_Stewart.Motor1_D, Index_Stewart.Motor6_D + 1):
            pid_table_list[2].append(self.stewart._vars[i].value())
        for i in range(Index_Stewart.Motor1_Gain, Index_Stewart.Motor6_Gain + 1):
            pid_table_list[3].append(self.stewart._vars[i].value())
        for i in range(Index_Stewart.Motor1_Deadband, Index_Stewart.Motor6_Deadband + 1):
            pid_table_list[4].append(self.stewart._vars[i].value())
        for row in range(5):
            for col in range(6):
                pid_table_list[row][col] =  float(pid_table_list[row][col])
                self.table.item(row, col).setText(str(pid_table_list[row][col]))

    def set_values(self):
        p_data = self.data[0]
        i_data = self.data[1]
        d_data = self.data[2]
        gain_data = self.data[3]
        deadband_data = self.data[4]
        PID_data = [p_data, i_data, d_data, gain_data, deadband_data]

        print("Current Table Data:")
        print('p_data',p_data)
        print('i_data',i_data)

        for i in range(5):
            for j in range(6):
                try:
                    PID_data[i][j] = float(PID_data[i][j])
                except:
                    PID_data[i][j] = 0.0
        print("Current Table Data:", PID_data)
        
        self.stewart.write_var([Index_Stewart.Motor1_P, p_data[0]],[Index_Stewart.Motor2_P, p_data[1]],[Index_Stewart.Motor3_P, p_data[2]],[Index_Stewart.Motor4_P, p_data[3]],[Index_Stewart.Motor5_P, p_data[4]],[Index_Stewart.Motor6_P, p_data[5]])
        self.stewart.write_var([Index_Stewart.Motor1_I, i_data[0]],[Index_Stewart.Motor2_I, i_data[1]],[Index_Stewart.Motor3_I, i_data[2]],[Index_Stewart.Motor4_I, i_data[3]],[Index_Stewart.Motor5_I, i_data[4]],[Index_Stewart.Motor6_I, i_data[5]])
        self.stewart.write_var([Index_Stewart.Motor1_D, d_data[0]],[Index_Stewart.Motor2_D, d_data[1]],[Index_Stewart.Motor3_D, d_data[2]],[Index_Stewart.Motor4_D, d_data[3]],[Index_Stewart.Motor5_D, d_data[4]],[Index_Stewart.Motor6_D, d_data[5]])
        self.stewart.write_var([Index_Stewart.Motor1_Gain, gain_data[0]],[Index_Stewart.Motor2_Gain, gain_data[1]],[Index_Stewart.Motor3_Gain, gain_data[2]],[Index_Stewart.Motor4_Gain, gain_data[3]],[Index_Stewart.Motor5_Gain, gain_data[4]],[Index_Stewart.Motor6_Gain, gain_data[5]])
        self.stewart.write_var([Index_Stewart.Motor1_Deadband, deadband_data[0]],[Index_Stewart.Motor2_Deadband, deadband_data[1]],[Index_Stewart.Motor3_Deadband, deadband_data[2]],[Index_Stewart.Motor4_Deadband, deadband_data[3]],[Index_Stewart.Motor5_Deadband, deadband_data[4]],[Index_Stewart.Motor6_Deadband, deadband_data[5]])

        print('p_data',p_data)
        print('i_data',i_data)
