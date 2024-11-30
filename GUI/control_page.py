from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class ControlPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Sayfaya iki buton ekleyelim
        button1 = QPushButton('Buton 1', self)
        button2 = QPushButton('Buton 2', self)

        layout.addWidget(button1)
        layout.addWidget(button2)

        self.setLayout(layout)
