from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QComboBox, QHeaderView
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from config_widgets.pid_table import PID_Table
from config_widgets.stewart_parameter_list import *


class CustomLineEdit(QLineEdit):
    def __init__(self, table_name, row, col, stewart, parent=None):
        super().__init__(parent)
        self.table_name = table_name  # Hangi tabloya ait olduğunu belirtiyor
        self.row = row
        self.col = col
        self.stewart = stewart

    def focusOutEvent(self, event):
        value = self.text()
        type_of_parameter = self.stewart._vars[int(self.row)].type()
        changeable = self.stewart._vars[int(self.row)].
        print("parameter type = ",type_of_parameter)
        #stewart.write_var([int(self.row), value] )
        print(f'Tablo: {self.table_name}, Satır: {self.row}, Sütun: {self.col}, Girilen Değer: {value}')
        super().focusOutEvent(event)


class ConfigPage(QWidget):
    def __init__(self, stewart):
        self.stewart = stewart
        super().__init__()
        self.table_data = {
            'defaults': {},
            'config': {},
            'offsets': {},
            'pid': {}
        }
        self.initUI()

        self.stewart.get_all_variable()
        
        

    def initUI(self):
        self.setWindowTitle('Config Page')
        self.setGeometry(100, 100, 900, 700)

        main_layout = QHBoxLayout()

        # Sol layout (Tablolar grubu)
        left_layout = QVBoxLayout()

        # Defaults tablosu
        self.defaults_table = self.create_table(
            stewart_parameter_list,
            'Config'
        )
        left_layout.addWidget(self.defaults_table)
        
        # PID tablosu
        self.pid_table = PID_Table(self.stewart)
        left_layout.addWidget(self.pid_table)
        main_layout.addLayout(left_layout)

        # Sağ layout (Butonlar ve diğer bileşenler)
        right_layout = QVBoxLayout()
        refresh_button = QPushButton('Refresh', self)
        calibrate_button = QPushButton('Calibrate', self)
        reboot_button = QPushButton('Reboot', self)
        eeprom_button = QPushButton('EEPROM SAVE', self)
        factory_reset_button = QPushButton('Factory Reset', self)

        right_layout.addWidget(refresh_button)
        right_layout.addWidget(calibrate_button)
        right_layout.addWidget(reboot_button)
        right_layout.addWidget(eeprom_button)
        right_layout.addWidget(factory_reset_button)

        # Resim ve ayarlar kısmı
        image_and_settings_layout = QHBoxLayout()
        image_label = QLabel(self)
        pixmap = QPixmap('GUI/images/stewart.png')
        if pixmap.isNull():
            pixmap = QPixmap(200, 200)
            pixmap.fill(Qt.gray)
        else:
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_and_settings_layout.addWidget(image_label)

        settings_layout = QVBoxLayout()
        settings_layout.addWidget(QLabel('Config Setting'))
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(['Option 1', 'Option 2', 'Option 3', 'Option 4'])
        settings_layout.addWidget(self.combo_box)
        image_and_settings_layout.addLayout(settings_layout)

        right_layout.addLayout(image_and_settings_layout)

        # Spacer
        right_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def create_table(self, parameters, title):
        rows = len(parameters)
        table = QTableWidget(rows, 2, self)
        table.setHorizontalHeaderLabels(['Parameter', 'Value'])
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        for row, parameter in enumerate(parameters):
            table.setItem(row, 0, QTableWidgetItem(parameter))
            
            line_edit = CustomLineEdit(title, row, 1, self.stewart ,self)  # Tablo adını da geçiriyoruz
            table.setCellWidget(row, 1, line_edit)
            table.item(row, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        return table
    
