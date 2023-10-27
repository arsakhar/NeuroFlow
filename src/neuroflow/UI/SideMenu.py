from PyQt5.QtWidgets import QFrame, QSizePolicy, QHBoxLayout, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon

from .Logo import Logo

from ..Helper.Resources import resource_path


# creates a side menu located on left side of main window
class SideMenu(QWidget):
    HOME_BUTTON = 0

    def __init__(self, parent):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)

        self.sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(self.centralFrame.sizePolicy().hasHeightForWidth())

        self.centralFrame.setSizePolicy(self.sizePolicy)

        self.centralFrame.setMinimumSize(QSize(70, 0))
        self.centralFrame.setMaximumSize(QSize(70, 16777215))

        self.centralFrame.setLayoutDirection(Qt.LeftToRight)
        self.centralFrame.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)

        self.logoFrame = QFrame(self.centralFrame)
        self.logoWidget = Logo(self.logoFrame)

        self.logoLayout = QHBoxLayout(self.logoFrame)
        self.logoLayout.setAlignment(Qt.AlignCenter)
        self.logoLayout.addWidget(self.logoWidget)

        self.btnsFrame = QFrame(self.centralFrame)

        self.homeBtn = MenuButton(self.btnsFrame)
        self.homeBtn.setIcon(QIcon(resource_path("icons/24x24/cil-home")))

        self.btnsLayout = QVBoxLayout(self.btnsFrame)
        self.btnsLayout.addWidget(self.homeBtn, alignment=Qt.AlignTop)

        self.centralLayout = QVBoxLayout(self.centralFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.centralLayout.addWidget(self.logoFrame, stretch=1, alignment=Qt.AlignTop)
        self.centralLayout.addWidget(self.btnsFrame, stretch=4)

        self.uiLayout = QHBoxLayout(self)
        self.uiLayout.addWidget(self.centralFrame)
        self.uiLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.uiLayout)


class MenuButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setIconSize(QSize(40, 40))

        self.setStyleSheet(u"QPushButton {"
                           "border: none;"
                           "background-color: transparent;"
                           "}"
                           "QPushButton:hover {"
                           "background-color: rgb(85, 170, 255);"
                           "}"
                           "QPushButton:pressed {"
                           "background-color: rgb(85, 170, 255);"
                           "}"
                           "QToolTip {"
                           "color:white;"
                           "background-color: black;"
                           "border: black solid 1px;"
                           "}")
