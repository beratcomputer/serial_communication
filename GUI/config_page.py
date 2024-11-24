from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout, QHeaderView, QGroupBox, QCheckBox, QComboBox
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def focusOutEvent(self, event):
        # Kutunun dışına tıklayınca tetiklenen fonksiyon
        value = self.text()  # Girilen değeri al
        print(f'Odak dışı girilen değer: {value}')
        # Varsayılan focusOutEvent işlevini çağır
        super().focusOutEvent(event)


class ConfigPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Ana pencere ayarları
        self.setWindowTitle('20x2 Tablo ve Butonlar')
        self.setGeometry(100, 100, 800, 600)

        # Ana yatay layout (sola tablo, sağa butonlar gelecek)
        main_layout = QHBoxLayout()

        # Tablo ve widget'lar için sol layout (tablo kısmı)
        table_layout = QVBoxLayout()

        # 20x4 tablo oluşturma
        self.table = QTableWidget(20, 4, self)
        self.table.setHorizontalHeaderLabels(['Parameter', 'Variable', 'Parameter', 'Variable'])

        # Sütun genişliğinin pencere boyutuna göre ayarlanması
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # İlk sütuna metin, ikinci sütuna QLineEdit ekleme
        for row in range(20):
            # Her hücreye metin ekleme
            item = QTableWidgetItem(f'Parameter {row + 1}')
            self.table.setItem(row, 0, item)
            item2 = QTableWidgetItem(f'Parameter {row + 1}')
            self.table.setItem(row, 2, item2)

            # Sayı girişi için QLineEdit ekleme
            line_edit = CustomLineEdit(self)
            line_edit.setPlaceholderText('Sayı girin')
            line_edit.returnPressed.connect(self.on_input_entered)  # Enter'a basıldığında tetiklenir
            self.table.setCellWidget(row, 1, line_edit)

            line_edit2 = CustomLineEdit(self)
            line_edit2.setPlaceholderText('Sayı girin')
            line_edit2.returnPressed.connect(self.on_input_entered)  # Enter'a basıldığında tetiklenir
            self.table.setCellWidget(row, 3, line_edit2)

        # Sol layout'a tablo ekleme
        table_layout.addWidget(self.table)

        # Sağ layout (butonlar, resim ve 5x1 tablo için)
        side_layout = QVBoxLayout()

        # 5 tane buton ekleme
        refresh_button = QPushButton(f'Refresh', self)
        side_layout.addWidget(refresh_button)
        reboot_button = QPushButton(f'Reboot ', self)
        side_layout.addWidget(reboot_button)
        eeprom_write_button = QPushButton(f'EEPROM SAVE', self)
        side_layout.addWidget(eeprom_write_button)
        factory_reset_button = QPushButton(f'Factory Reset', self)
        side_layout.addWidget(factory_reset_button)

        # Resim ve yanına metin ve seçim kutusu eklemek için yatay layout
        image_and_settings_layout = QHBoxLayout()  # Hızalı (Horizontal) layout kullanıyoruz

        # Resim ekleme
        self.image_label = QLabel(self)
        pixmap = QPixmap('GUI/images/stewart.png')  # Yerel dosyadan resim yükleyin
        if pixmap.isNull():  # Eğer resim bulunamazsa, hata kontrolü yapalım
            pixmap = QPixmap(200, 200)  # Placeholder boyutunda gri bir resim ekle
            pixmap.fill(Qt.gray)
        else:
            pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        image_and_settings_layout.addWidget(self.image_label)  # Resmi layout'a ekle

        # Metin ve kutucuklar için dikey layout
        settings_layout = QVBoxLayout()

        # Metin ekleme
        config_label = QLabel("Config Setting", self)
        settings_layout.addWidget(config_label)

        # QComboBox ekleme (4 tane seçenek)
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(['Option 1', 'Option 2', 'Option 3', 'Option 4'])
        settings_layout.addWidget(self.combo_box)

        # Ayarları içeren dikey layout'u yatay layout'a ekleme
        image_and_settings_layout.addLayout(settings_layout)

        # side_layout'a (butonlar ile tablo arasına) image_and_settings_layout'ı ekleme
        side_layout.addLayout(image_and_settings_layout)
        # Altına 5x1 tablo (5 satır, 1 sütun)
        self.small_table = QTableWidget(8, 2, self)
        self.small_table.setHorizontalHeaderLabels(['Parameter', 'Value'])
        header2 = self.small_table.horizontalHeader()
        header2.setSectionResizeMode(QHeaderView.Stretch)
        for row in range(8):
            self.small_table.setItem(row, 0, QTableWidgetItem(f'Param {row + 1}'))

        side_layout.addWidget(self.small_table)

        # Spacer (butonlar ve tablo arasında boşluk bırakmak için)
        side_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Ana layout'a sol ve sağ layoutları ekleme
        main_layout.addLayout(table_layout)  # Sola tablo
        main_layout.addLayout(side_layout)   # Sağa butonlar ve diğer bileşenler

        # Ana layout'u pencereye ekleme
        self.setLayout(main_layout)

    def on_input_entered(self):
        # Enter'a basıldığında tetiklenen fonksiyon
        line_edit = self.sender()  # Hangi QLineEdit'in sinyal gönderdiğini al
        value = line_edit.text()  # Girilen değeri al
        print(f'Enter ile girilen değer: {value}')
