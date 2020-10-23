from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from scripts.Helper.Resources import *


class Logo(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.label = QLabel(self.centralFrame)
        self.pixmap = QPixmap(resource_path('icons/icons8-brain-64.png'))
        self.pixmap = self.pixmap.scaled(40, 40, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.label)
        self.centralLayout.setAlignment(Qt.AlignCenter)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)
