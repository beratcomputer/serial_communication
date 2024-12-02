from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QComboBox, QHeaderView
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from config_widgets.pid_table import PID_Table


class CustomLineEdit(QLineEdit):
    def __init__(self, table_name, row, col, parent=None):
        super().__init__(parent)
        self.table_name = table_name  # Hangi tabloya ait olduğunu belirtiyor
        self.row = row
        self.col = col

    def focusOutEvent(self, event):
        value = self.text()
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
       

    def initUI(self):
        self.setWindowTitle('Config Page')
        self.setGeometry(100, 100, 900, 700)

        main_layout = QHBoxLayout()

        # Sol layout (Tablolar grubu)
        left_layout = QVBoxLayout()

        # Defaults tablosu
        self.defaults_table = self.create_table(
            ['Header', 'Device ID', 'Hardware Version', 'Software Version', 'Baudrate'],
            'Defaults'
        )
        left_layout.addWidget(self.defaults_table)

        # Config tablosu
        self.config_table = self.create_table(
            ['Motor Max Speeds', 'Device Loop Frequency', 'Motor CPRs'],
            'Config'
        )
        left_layout.addWidget(self.config_table)

        # Offsets tablosu
        self.offsets_table = self.create_table(
            ['Offset X', 'Offset Y', 'Offset Z'],
            'Offsets'
        )
        left_layout.addWidget(self.offsets_table)

        # PID tablosu
        self.pid_table = QTableWidget(5, 7, self)
        self.pid_table.setHorizontalHeaderLabels(['1', '2', '3', '4', '5', '6', 'ALL'])
        self.pid_table.setVerticalHeaderLabels(['P', 'I', 'D', 'Deadband', 'Gain'])

        # PID tablosu verilerini sözlükte saklamak için yapı
        self.table_data['pid'] = {}

        for row in range(5):  # 5 satır
            self.table_data['pid'][row] = {}  # Her satır için ayrı bir sözlük
            for col in range(7):
                if col == 6:  # ALL sütunu
                    line_edit = CustomLineEdit('pid', row, col, self)
                    line_edit.returnPressed.connect(self.on_all_input)
                else:  # Diğer sütunlar
                    line_edit = CustomLineEdit(row, col, self)
                    line_edit.textChanged.connect(lambda value, r=row, c=col: self.update_table_data('pid', r, c, value))
                    #line_edit.textChanged.connect(lambda value, r=row, t=title: self.update_table_data(t, r, value))

                self.pid_table.setCellWidget(row, col, line_edit)

        left_layout.addWidget(QLabel('PID Settings'))
        left_layout.addWidget(self.pid_table)

        main_layout.addLayout(left_layout)


        # Sağ layout (Butonlar ve diğer bileşenler)
        right_layout = QVBoxLayout()
        refresh_button = QPushButton('Refresh', self)
        reboot_button = QPushButton('Reboot', self)
        eeprom_button = QPushButton('EEPROM SAVE', self)
        factory_reset_button = QPushButton('Factory Reset', self)

        right_layout.addWidget(refresh_button)
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
            
            line_edit = CustomLineEdit(title, row, 1, self)  # Tablo adını da geçiriyoruz
            line_edit.textChanged.connect(lambda value, r=row, t=title: self.update_table_data(t, r, parameter, value))
            table.setCellWidget(row, 1, line_edit)
            table.item(row, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        return table


    def on_all_input(self):
        line_edit = self.sender()
        value = line_edit.text()
        indexes = self.pid_table.indexAt(line_edit.pos())
        if indexes.isValid():
            row = indexes.row()
            for col in range(6):  # 1-6 sütunları
                widget = self.pid_table.cellWidget(row, col)
                if isinstance(widget, QLineEdit):
                    widget.setText(value)
                    self.update_table_data('pid', (row, col), value)  # Sözlüğü de güncelle

    def update_table_data(self, table_name, row, col, value):
        if table_name not in self.table_data:
            return

        if row not in self.table_data[table_name]:
            self.table_data[table_name][row] = {}

        self.table_data[table_name][row][col] = value
        print(f'{table_name} tablosunda [Satır: {row}, Sütun: {col}] için güncellenen değer: {value}')

