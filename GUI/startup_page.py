import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QLineEdit,
    QHeaderView, QCheckBox, QLabel, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from main_app import MainApp  # İkinci pencereyi içe aktar
from serial.tools import list_ports

import os

# src/python klasörünü sys.path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'python')))

# subthree modülünü import et
from acrome_embedded_devices import *

class StartupPage(QMainWindow):
    """Başlangıç Penceresi."""
    def __init__(self):
        super().__init__()
        self.device_list = []  # Eklenen cihaz nesnelerini saklamak için bir liste
        self.selected_port = None
        # Diğer bileşenler...
        self.setWindowTitle("Port Yönetim Arayüzü")
        self.setGeometry(100, 100, 900, 600)
        
        # Ana Widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Ana Layout
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Sol Panel (Görseller için alan)
        left_panel = QVBoxLayout()
        left_placeholder = QLabel("Buraya Görseller Eklenebilir")
        left_placeholder.setFrameStyle(QFrame.Box | QFrame.Plain)
        left_placeholder.setAlignment(Qt.AlignCenter)
        left_placeholder.setMinimumWidth(250)
        left_panel.addWidget(left_placeholder)
        main_layout.addLayout(left_panel)
        
        # Sağ Panel (Ana Fonksiyonlar)
        right_panel = QVBoxLayout()
        main_layout.addLayout(right_panel)
        
        # Port seçimi ve scan butonu
        port_layout = QHBoxLayout()
        self.port_selector = QComboBox()
        self.port_selector.addItem("Port Seçiniz")
        port_layout.addWidget(self.port_selector)
        self.populate_ports()
        if self.port_selector.count() >= 1:  # "Port Seçiniz" hariç başka seçenek varsa
            self.port_selector.setCurrentIndex(0)  # İlk geçerli portu seç
            self.selected_port = self.port_selector.currentText()  # Seçilen portu ata
            print(f"Başlangıçta seçilen port: {self.selected_port}")

        self.port_selector.currentTextChanged.connect(self.on_port_selected)
        
        self.scan_button = QPushButton("Scan")
        self.scan_button.setStyleSheet("""
            padding: 8px 16px; 
            font-size: 14px; 
            background-color: #902020; 
            color: white; 
            border: 2px solid #000000;  /* Siyah kenarlık */
            border-radius: 4px;
        """)
        self.scan_button.clicked.connect(self.scan_ports)
        port_layout.addWidget(self.scan_button)
        
        right_panel.addLayout(port_layout)

        
        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "İsim"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        right_panel.addWidget(self.table)
        
        # Manuel ekleme kontrolü
        self.manual_add_checkbox = QCheckBox("Manuel olarak eklemek istiyorum")
        self.manual_add_checkbox.stateChanged.connect(self.toggle_add_widgets)
        right_panel.addWidget(self.manual_add_checkbox)
        
        # Ekleme Alanı (Başlangıçta gizli)
        self.add_layout = QHBoxLayout()
        
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID")
        self.add_layout.addWidget(self.id_input)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("İsim")
        self.add_layout.addWidget(self.name_input)
        
        self.add_button = QPushButton("Ekle")
        self.add_button.clicked.connect(self.add_row)
        self.add_layout.addWidget(self.add_button)
        
        self.add_widgets = QWidget()
        self.add_widgets.setLayout(self.add_layout)
        self.add_widgets.setVisible(False)
        right_panel.addWidget(self.add_widgets)
        
        # Start Butonu
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet(
            "padding: 10px 20px; font-size: 24px; background-color: #902020; color: white; border-radius: 10px;"
        )
        self.start_button.clicked.connect(self.open_main_app)
        right_panel.addWidget(self.start_button)

        print(self.selected_port)

    def on_port_selected(self, port):
        if port != "Port Seçiniz" and port != "Port Bulunamadı":  # Geçersiz seçimleri kontrol et
            self.selected_port = port
            print(f"Seçilen port: {self.selected_port}")
        else:
            self.selected_port = None  # Geçersiz seçim durumunda değişkeni temizle

    
    def toggle_add_widgets(self, state):
        self.add_widgets.setVisible(state == Qt.Checked)
    
    def add_row(self, from_scan = False, id_from_scan = None):
        if from_scan == False:
            id_text = self.id_input.text()
            name_text = self.name_input.text()
            
        else:
            id_text = id_from_scan
            name_text = " "
        
        if id_text:
            row_count = self.table.rowCount()
            self.table.insertRow(row_count)
            self.table.setItem(row_count, 0, QTableWidgetItem(str(id_text)))
            self.table.setItem(row_count, 1, QTableWidgetItem(str(name_text)))
            # Yeni cihaz nesnesi oluşturma
            self.device_list.append(int(id_text))
            self.id_input.clear()
            self.name_input.clear()
        else:
            print("Lütfen ID ve İsim alanlarını doldurun!")
    
    def open_main_app(self):
        if(self.device_list == []):
            self.show_error_message("No device added!")
            return
        print(self.device_list)

        self.main_app = MainApp(device_list=self.device_list, port=self.selected_port)  # İkinci pencereyi oluştur
        self.main_app.show()       # İkinci pencereyi göster
        self.close()               # Bu pencereyi kapat

    def populate_ports(self):
        """Kullanılabilir portları doldurur."""
        self.port_selector.clear()  # Mevcut öğeleri temizle
        ports = list_ports.comports()  # Mevcut portları al
        for port in ports:
            self.port_selector.addItem(port.device)  # Port isimlerini ekle
        if not ports:
            self.port_selector.addItem("Port Bulunamadı")  # Eğer port yoksa bir mesaj ekle
    
    def scan_ports(self):
        print("Scan butonuna basıldı, farklı bir işlev çağrılabilir.")
        #scanned_list = scan_Stewarts(self.selected_port)
        scanned_list = [0,1,3,56]
        for id in scanned_list:
            self.add_row(True, id)
        
    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)  # Hata ikonunu ayarla
        msg_box.setWindowTitle("Error")
        msg_box.geometry()
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()  # Mesaj kutusunu göster ve kullanıcı yanıtını bekle


if __name__ == '__main__':
    app = QApplication(sys.argv)
    startup_page = StartupPage()
    startup_page.show()
    sys.exit(app.exec_())
