from PyQt5.QtWidgets import QFrame, QSizePolicy, QHBoxLayout, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtCore import pyqtSignal

from scripts.Helper.Resources import *

"""
Creates a custom title bar for main window to use in place of Windows default title bar
"""
class TitleBar(QWidget):
    def __init__(self, ui_main):
        super().__init__()

        self.ui_main = ui_main

        self.initUI()

        self.closeBtn.closeClicked.connect(self.ui_main.close)
        self.resizeBtn.showNormal.connect(self.ui_main.showNormal)
        self.resizeBtn.showMaximized.connect(self.ui_main.showMaximized)
        self.minimizeBtn.showMinimized.connect(self.ui_main.showMinimized)

    def initUI(self):
        self.sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)

        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setMinimumSize(QSize(0, 40))
        self.centralFrame.setMaximumSize(QSize(16777215, 42))
        self.centralFrame.setStyleSheet(u"background-color: rgba(27, 29, 35, 255)")

        """
        Title Frame, Label, and Layout
        """
        self.titleFrame = QFrame(self.centralFrame)
        self.sizePolicy.setHeightForWidth(self.titleFrame.sizePolicy().hasHeightForWidth())
        self.titleFrame.setSizePolicy(self.sizePolicy)
        self.titleFrame.setFrameShape(QFrame.NoFrame)
        self.titleFrame.setFrameShadow(QFrame.Raised)
        self.titleFrame.setContentsMargins(0, 0, 0, 0)
        self.titleFrame.setStyleSheet("border: none;")

        self.label = TitleBarLabel(self.titleFrame)

        self.titleFrameLayout = QHBoxLayout(self.titleFrame)
        self.titleFrameLayout.addWidget(self.label)
        self.titleFrameLayout.setSpacing(0)
        self.titleFrameLayout.setContentsMargins(5, 0, 10, 0)

        """
        Buttons Frame, Buttons, and Layout
        """
        self.btnsFrame = QFrame(self.centralFrame)
        self.sizePolicy.setHeightForWidth(self.btnsFrame.sizePolicy().hasHeightForWidth())
        self.btnsFrame.setSizePolicy(self.sizePolicy)
        self.btnsFrame.setMaximumSize(QSize(120, 16777215))
        self.btnsFrame.setFrameShape(QFrame.NoFrame)
        self.btnsFrame.setFrameShadow(QFrame.Raised)
        self.btnsFrame.setContentsMargins(0, 0, 0, 0)

        self.minimizeBtn = MinimizeButton(self.btnsFrame)
        self.resizeBtn = ResizeButton(self.btnsFrame)
        self.closeBtn = CloseButton(self.btnsFrame)

        self.btnsLayout = QHBoxLayout(self.btnsFrame)
        self.btnsLayout.addWidget(self.minimizeBtn)
        self.btnsLayout.addWidget(self.resizeBtn)
        self.btnsLayout.addWidget(self.closeBtn)
        self.btnsLayout.setSpacing(0)
        self.btnsLayout.setContentsMargins(0, 0, 0, 0)

        """
        Central Layout
        """
        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.titleFrame)
        self.centralLayout.addWidget(self.btnsFrame, 0, Qt.AlignRight)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        """
        UI Layout
        """
        self.uiLayout = QHBoxLayout(self)
        self.uiLayout.addWidget(self.centralFrame)
        self.uiLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.uiLayout)

    def mouseMoveEvent(self, ev):
        self.ui_main.moveWindow(ev)


class MinimizeButton(QPushButton):
    showMinimized = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.clicked.connect(self.minimize)

        self.initUI()

    def initUI(self):
        self.setObjectName(u"minimizeBtn")

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.setMinimumSize(QSize(40, 0))
        self.setMaximumSize(QSize(40, 16777215))
        self.setStyleSheet(u"QPushButton {"
                           "border: none;"
                           "background-color: transparent;"
                           "}"
                           "QPushButton:hover {"
                           "background-color: rgb(52, 59, 72);"
                           "}"
                           "QPushButton:pressed {"
                           "background-color: rgb(85, 170, 255);"
                           "}"
                           "QToolTip {"
                           "color:white;"
                           "background-color: black;"
                           "border: black solid 1px;"
                           "}")

        icon = QIcon()
        icon.addFile(resource_path("icons/16x16/cil-window-minimize.png"),
                     QSize(), QIcon.Normal, QIcon.Off)
        self.setIcon(icon)
        self.setToolTip("Minimize")
        self.setContentsMargins(0, 0, 0, 0)

    def minimize(self):
        self.showMinimized.emit()


class ResizeButton(QPushButton):
    showNormal = pyqtSignal()
    showMaximized = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.clicked.connect(self.resize)
        self.maximized = False

        self.initUI()

    def initUI(self):
        self.setObjectName(u"maximizeBtn")

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.setMinimumSize(QSize(40, 0))
        self.setMaximumSize(QSize(40, 16777215))
        self.setStyleSheet(u"QPushButton {"
                           "border: none;"
                           "background-color: transparent;"
                           "}"
                           "QPushButton:hover {"
                           "background-color: rgb(52, 59, 72);"
                           "}"
                           "QPushButton:pressed {"
                           "background-color: rgb(85, 170, 255);"
                           "}"
                           "QToolTip {"
                           "color:white;"
                           "background-color: black;"
                           "border: black solid 1px;"
                           "}")
        icon = QIcon()
        icon.addFile(resource_path("icons/16x16/cil-window-maximize.png"),
                     QSize(), QIcon.Normal, QIcon.Off)
        self.setIcon(icon)
        self.setToolTip("Maximize")
        self.setContentsMargins(0, 0, 0, 0)

    def resize(self):
        if self.maximized:
            self.showNormal.emit()
            self.setToolTip("Maximize")
            self.setIcon(QtGui.QIcon("icons/16x16/cil-window-maximize.png"))

        else:
            self.showMaximized.emit()
            self.setToolTip("Restore")
            self.setIcon(QtGui.QIcon(resource_path("icons/16x16/cil-window-restore.png")))

        self.maximized = not self.maximized


class CloseButton(QPushButton):
    closeClicked = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.clicked.connect(self.close)

        self.initUI()

    def initUI(self):
        self.setObjectName(u"closeBtn")

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.setMinimumSize(QSize(40, 0))
        self.setMaximumSize(QSize(40, 16777215))

        self.setStyleSheet(u"QPushButton {"
                           "border: none;"
                           "background-color: transparent;"
                           "}"
                           "QPushButton:hover {"
                           "background-color: rgb(52, 59, 72);"
                           "}"
                           "QPushButton:pressed {"
                           "background-color: rgb(85, 170, 255);"
                           "}"
                           "QToolTip {"
                           "color:white;"
                           "background-color: black;"
                           "border: black solid 1px;"
                           "}")

        icon = QIcon()
        icon.addFile(resource_path("icons/16x16/cil-x.png"),
                     QSize(), QIcon.Normal, QIcon.Off)
        self.setIcon(icon)
        self.setToolTip("Close")
        self.setContentsMargins(0, 0, 0, 0)

    def close(self):
        self.closeClicked.emit()


class TitleBarLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setText("NeuroFlow - Flow Dynamics Software")
        self.setObjectName("titleBarIcon")
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)
        self.setStyleSheet(u"background: transparent;\n""")
        self.setContentsMargins(0, 0, 0, 0)
