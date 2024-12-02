import sys
from PyQt5.QtWidgets import (
    QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QCheckBox, QPushButton, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class config_Table(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("PyQt5 Tablo")

        # Tablo oluştur
        self.table = QTableWidget(6, 7)  # 6 satır: 5 veri + 1 checkbox
        self.table.setHorizontalHeaderLabels(["1", "2", "3", "4", "5", "6", "ALL"])
        self.table.setVerticalHeaderLabels(["P", "I", "D", "Gain", "Deadbend", ""])
        
        # Enable ALL Checkbox'ı ekle
        self.all_checkbox = QCheckBox("Enable ALL")
        self.all_checkbox.stateChanged.connect(self.toggle_all)
        self.table.setCellWidget(5, 6, self.all_checkbox)

        # Varsayılan düzenleme davranışı
        self.toggle_all(Qt.Unchecked)

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

    def set_values(self):
        if self.all_checkbox.isChecked():
            for row in range(5):
                all_item = self.table.item(row, 6)
                if all_item and all_item.text():
                    all_value = all_item.text()
                    for col in range(6):  # 1, 2, 3, 4, 5, 6 sütunlarına kopyala
                        self.table.item(row, col).setText(all_value)
        else:
            print("Set işlemine gerek yok.")
