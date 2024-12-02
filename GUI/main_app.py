import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from config_page import ConfigPage
from control_page import ControlPage


class MainApp(QWidget):
    def __init__(self, device_list):
        super().__init__()
        self.device_list = device_list  # Cihaz listesi
        self.one_device = device_list[0]
        self.initUI()

    def initUI(self):
        # Ana pencere ayarları
        self.setWindowTitle('ACROME Embedded Stewart')
        self.setGeometry(100, 100, 1000, 600)

        # QTabWidget (Sekmeler) oluşturma
        self.tabs = QTabWidget(self)

        # Sayfaları oluştur
        self.config_page = ConfigPage()  # Config sayfası
        self.control_page = ControlPage()  # Control sayfası

        # Sekmelere sayfaları ekleme
        self.tabs.addTab(self.config_page, "Config")
        self.tabs.addTab(self.control_page, "Control")

        # Ana layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)



