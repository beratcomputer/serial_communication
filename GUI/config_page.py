from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QComboBox, QHeaderView
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def focusOutEvent(self, event):
        value = self.text()
        print(f'Odak dışı girilen değer: {value}')
        super().focusOutEvent(event)


class ConfigPage(QWidget):
    def __init__(self):
        super().__init__()
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

        for row in range(5):  # Artık 5 satır var
            for col in range(7):
                if col == 6:  # ALL sütununa bir QLineEdit ekle
                    line_edit = CustomLineEdit(self)
                    line_edit.returnPressed.connect(self.on_all_input)
                    self.pid_table.setCellWidget(row, col, line_edit)
                else:  # Diğer sütunlara QLineEdit ekle
                    line_edit = CustomLineEdit(self)
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
            table.setItem(row, 0, QTableWidgetItem(parameter))  # Parameter hücresi sabit
            line_edit = CustomLineEdit(self)  # Value hücresi düzenlenebilir
            table.setCellWidget(row, 1, line_edit)
            table.item(row, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Parameter hücresi düzenlenemez

        return table

    def on_all_input(self):
        line_edit = self.sender()
        value = line_edit.text()
        print(f'ALL sütununa girilen değer: {value}')

        # Satırdaki diğer hücrelere ALL'a girilen değeri yaz
        indexes = self.pid_table.indexAt(line_edit.pos())
        if indexes.isValid():
            row = indexes.row()
            for col in range(6):  # 1-6 sütunları
                widget = self.pid_table.cellWidget(row, col)
                if isinstance(widget, QLineEdit):
                    widget.setText(value)
