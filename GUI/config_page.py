from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QComboBox, QHeaderView, QProgressDialog, QApplication
)
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt
from config_widgets.pid_table import PID_Table
from config_widgets.stewart_parameter_list import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'python')))
# subthree modülünü import et
from acrome_embedded_devices import *


motor_size_indexes = ['2 Inches', '4 Inches', '8 Inches', '12 Inches']

# Motor boyutuna gore kontrol limitlerini belirlemeyi unutma!



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
        writeable = self.stewart._vars[int(self.row)].writeable()

        if writeable == True and value != '':
            if type_of_parameter == 'B' or type_of_parameter == 'I':
                value = int(float(value))
            elif  type_of_parameter == 'f':
                value = float(value)
            else:
                value = int(value)
            
            self.stewart.write_var([int(self.row), value])
        super().focusOutEvent(event)


class ConfigPage(QWidget):
    def __init__(self, stewart):
        self.stewart = stewart
        super().__init__()

        self.initUI()

        self.pid_window = PID_Table(self.stewart)  # PID penceresi için bir referans
        self.pid_window.hide()
        
        # Buraya Defaults tablosunda bazi seyler eklemek istiyorum.
        # hangi fonksiyonlari kullanmaliyim.

        self.no_changable_vars = [Index_Stewart.Header, Index_Stewart.PackageSize, Index_Stewart.Command, Index_Stewart.HardwareVersion,
                             Index_Stewart.SoftwareVersion, Index_Stewart.Baudrate, Index_Stewart.Status, Index_Stewart.MotorSizes, Index_Stewart.OperationMode] 

        self.refresh_all_data()
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
        

        # PID tablosu butonu
        self.toggle_pid_button = QPushButton("Open PID Table", self)
        self.toggle_pid_button.clicked.connect(self.toggle_pid_table)
        left_layout.addWidget(self.toggle_pid_button)

        main_layout.addLayout(left_layout)

        # Sağ layout (Butonlar ve diğer bileşenler)
        right_layout = QVBoxLayout()
        
        # Connection check layout
        self.connection_check_button = QPushButton('Connection Check', self)
        self.connection_indicator = QLabel(self)
        self.connection_indicator.setFixedSize(20, 20)
        self.connection_indicator.setStyleSheet("background-color: green; border: 1px solid black;")
        connection_check_layout = QHBoxLayout()
        connection_check_layout.addWidget(self.connection_check_button)
        connection_check_layout.addWidget(self.connection_indicator)

        self.refresh_button = QPushButton('Refresh', self)
        self.calibrate_button = QPushButton('Calibrate', self)
        self.reboot_button = QPushButton('Reboot', self)
        self.eeprom_button = QPushButton('EEPROM SAVE', self)
        self.factory_reset_button = QPushButton('Factory Reset', self)

        
        right_layout.addLayout(connection_check_layout)
        right_layout.addWidget(self.refresh_button)
        right_layout.addWidget(self.calibrate_button)
        right_layout.addWidget(self.reboot_button)
        right_layout.addWidget(self.eeprom_button)
        right_layout.addWidget(self.factory_reset_button)


        self.connection_check_button.clicked.connect(self.connection_check)
        self.refresh_button.clicked.connect(self.refresh_all_data)
        self.calibrate_button.clicked.connect(self.calibrate)
        self.reboot_button.clicked.connect(self.reboot)
        self.eeprom_button.clicked.connect(self.eeprom_save)
        self.factory_reset_button.clicked.connect(self.factory_reset)

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
        self.combo_box.addItems(['2 Inches', '4 Inches', '8 Inches', '12 Inches'])
        settings_layout.addWidget(self.combo_box)
        image_and_settings_layout.addLayout(settings_layout)
        initial_motor_size = motor_size_indexes[self.stewart._vars[Index_Stewart.MotorSizes].value()]
        self.combo_box.setCurrentText(initial_motor_size)
        self.combo_box.currentTextChanged.connect(self.motor_size_selection)

        right_layout.addLayout(image_and_settings_layout)

        # Spacer
        right_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def connection_check(self):
        if self.stewart.ping():
            self.connection_indicator.setStyleSheet("background-color: green; border: 1px solid black;")
        else:
            self.connection_indicator.setStyleSheet("background-color: red; border: 1px solid black;")

    def reboot(self):
        self.stewart.reboot()

    def eeprom_save(self):
        self.stewart.eeprom_save()

    def factory_reset(self):
        self.stewart.factory_reset()


    def refresh_all_data(self):
        # Bekleme animasyonu oluştur
        progress_dialog = QProgressDialog("Refreshing data...", "Cancel", 0, 0, self)
        progress_dialog.setWindowTitle("Refreshing")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setAutoClose(True)
        progress_dialog.setAutoReset(True)
        progress_dialog.show()
        QApplication.processEvents() 

        try:
            self.stewart.get_all_variable()  # Veri yenileme işlemi
            column = 1
            for i in self.stewart._vars:
                line_edit = CustomLineEdit('Config', int(i.index()), column, self.stewart, self)  # CustomLineEdit oluştur
                line_edit.setText(str(i.value()))  # Değeri ayarla
                self.defaults_table.setCellWidget(int(i.index()), column, line_edit)  # Hücreye widget olarak ekle

            for row in self.no_changable_vars:
                # Value sütunu için işlem
                cell_widget = self.defaults_table.cellWidget(row, 1)
                if isinstance(cell_widget, QLineEdit):
                    cell_widget.setReadOnly(True)  # Kullanıcının düzenlemesini engelle

                    # Renk değişikliği (gri arka plan)
                    cell_widget.setStyleSheet("background-color: lightgray; color: black;")

                # Parameter sütununu düzenlenemez yap
                parameter_item = self.defaults_table.item(row, 0)
                if parameter_item:
                    parameter_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    parameter_item.setBackground(QColor("lightgray"))  # Gri arka plan

            self.pid_window.upload_data()

        finally:
            # İşlem tamamlandıktan sonra animasyonu kapat
            progress_dialog.close()

    def calibrate(self):
        progress_dialog = QProgressDialog("Calibrating...", "Cancel", 0, 0, self)
        progress_dialog.setWindowTitle("Calibration")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setAutoClose(True)
        progress_dialog.setAutoReset(True)
        progress_dialog.show()
        QApplication.processEvents()
        try:
            self.stewart.calibrate()
        finally:
            progress_dialog.close()



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
    
    def toggle_pid_table(self):
        """PID tablosunun görünürlük durumunu değiştirir."""
        if self.pid_window.isVisible():
            self.pid_window.hide()
        else:
            self.pid_window.show()

    def motor_size_selection(self, selected_text):
        print(f"Selected config: {selected_text}")
        # Burada seçime göre istediğiniz işlemi yapabilirsiniz
        if selected_text == "2 Inches":
            self.stewart.write_var([Index_Stewart.MotorSizes, 0])
        elif selected_text == "4 Inches":
            self.stewart.write_var([Index_Stewart.MotorSizes, 1])
        elif selected_text == "8 Inches":
            self.stewart.write_var([Index_Stewart.MotorSizes, 2])
        elif selected_text == "12 Inches":
            self.stewart.write_var([Index_Stewart.MotorSizes, 3])
