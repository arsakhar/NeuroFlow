from PyQt5.QtWidgets import QToolButton, QWidgetAction, QFrame, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal

from ...Helper.ColorPicker import PaletteGrid
from ...Helper.Resources import *

"""
Widget to create overlay buttons
"""
class OverlayButton(QToolButton):
    overlaySelected = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)

        self.noneIconGraphic = None
        self.overlayColor = None

        self.initUI()
        self.is_pressed = False  # Track button state

        self.popup.palette.selected.connect(self.overlayUpdated)

    def initUI(self):
        self.popup = Action(self)
        self.addAction(self.popup)

        self.setPopupMode(QToolButton.InstantPopup)

        self.noneIconGraphic = QIcon(resource_path("icons/24x24/cil-pencil.png"))
        self.setIcon(self.noneIconGraphic)

    def newPatient(self, patient):
        self.overlayColor = None
        self.setIcon(self.noneIconGraphic)

    def overlayUpdated(self, color):
        self.overlayColor = color

        self.overlaySelected.emit(color)

    def mousePressEvent(self, event):
        self.is_pressed = not self.is_pressed

        if self.is_pressed:
            super().mousePressEvent(event)

            self.setDown(True)

        else:
            self.setDown(False)
            self.overlayUpdated(None)


class Action(QWidgetAction):
    def __init__(self, parent):
        super().__init__(parent)

        self.colorPicker = None
        self.palette = None

        self.initUI()

    def initUI(self):
        self.colorPicker = ColorPicker()
        self.palette = self.colorPicker._palette

        self.setDefaultWidget(self.colorPicker)


class ColorPicker(QWidget):
    def __init__(self):
        super().__init__()

        self._palette = None
        self._color = None

        self.initUI()

        self._palette.selected.connect(self.setColor)

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)

        self._palette = PaletteGrid('category10', n_columns=4)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self._palette)
        self.centralLayout.setAlignment(Qt.AlignCenter)
        self.centralLayout.setContentsMargins(3, 3, 3, 3)

        self.setLayout(self.centralLayout)

    def setColor(self, color):
        self._color = color
