import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from config_page import ConfigPage
from control_page import ControlPage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'python')))
# subthree modülünü import et
from acrome_embedded_devices import *

class MainApp(QWidget):
    def __init__(self, device_list, port):
        super().__init__()
        self.device_list = device_list  # Cihaz listesi
        self.one_device = Stewart(device_list[0], port)

        self.initUI()

    def initUI(self):
        # Ana pencere ayarları
        self.setWindowTitle('ACROME Embedded Stewart')
        self.setGeometry(100, 100, 1000, 600)

        # QTabWidget (Sekmeler) oluşturma
        self.tabs = QTabWidget(self)

        # Sayfaları oluştur
        self.config_page = ConfigPage(self.one_device)  # Config sayfası
        self.control_page = ControlPage(self.one_device)  # Control sayfası

        # Sekmelere sayfaları ekleme
        self.tabs.addTab(self.config_page, "Config")
        self.tabs.addTab(self.control_page, "Control")

        # Ana layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)



