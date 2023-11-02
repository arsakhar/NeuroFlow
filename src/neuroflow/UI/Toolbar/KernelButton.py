from PyQt5.QtWidgets import QToolButton, QWidgetAction, QLabel, QWidget, QFrame, QHBoxLayout, QSlider
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSignal

from ...Helper.Resources import *

"""
Widget to create kernel buttons
"""
class KernelButton(QToolButton):
    kernelSelected = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)

        self.noneIconGraphic = None
        self.kernelSize = 1

        self.initUI()
        self.is_pressed = False  # Track button state

        self.popup.kernel.valueChanged.connect(self.kernelUpdated)

    def initUI(self):
        self.popup = Action(self)

        self.setPopupMode(QToolButton.InstantPopup)

        self.setContentsMargins(0, 0, 0, 0)

        self.addAction(self.popup)

        self.noneIconGraphic = QIcon(resource_path("icons/paint-brush.png"))
        self.setIcon(self.noneIconGraphic)

    def kernelUpdated(self, kernelSize):
        if kernelSize == 0:
            self.kernelSize = None
        else:
            self.kernelSize = kernelSize

        self.kernelSelected.emit(kernelSize)

    def mousePressEvent(self, event):
        self.is_pressed = not self.is_pressed

        if self.is_pressed:
            super().mousePressEvent(event)

            self.setDown(True)

        else:
            self.setDown(False)
            self.kernelUpdated(0)


class Action(QWidgetAction):
    def __init__(self, parent):
        super().__init__(parent)

        self.slider = None
        self.kernel = None

        self.initUI()

    def initUI(self):
        self.slider = Slider()
        self.kernel = self.slider._slider

        self.setDefaultWidget(self.slider)


class Slider(QWidget):
    def __init__(self):
        super().__init__()

        self._slider = None
        self._value = None

        self.initUI()

        self._slider.valueChanged.connect(self.updateLabel)

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)

        self._slider = QSlider(Qt.Horizontal)
        self._slider.setMinimum(0)
        self._slider.setMaximum(16)
        self._slider.setValue(0)
        self._slider.setFixedSize(QSize(100, 25))
        self._slider.setStyleSheet(u"QSlider::handle:horizontal {"
                                   u"background-color: rgb(85, 170, 255);}")

        self._value = QLabel()
        self._value.setText('0')
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self._value.setFont(font)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self._slider)
        self.centralLayout.addWidget(self._value)
        self.centralLayout.setAlignment(Qt.AlignCenter)
        self.centralLayout.setContentsMargins(3, 3, 3, 3)

        self.setLayout(self.centralLayout)

    def updateLabel(self, value):
        self._value.setText(str(value))
