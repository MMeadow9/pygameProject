import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget
from PyQt5.QtCore import QSize


text = [
    "None"
]

class GuideRu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Guide")
        self.initUI()

    def initUI(self):
        self.resize(QSize(400, 400))

