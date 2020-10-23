from PyQt5.QtWidgets import QToolButton, QWidgetAction, QFrame, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal

from scripts.Helper.ColorMapPicker import PaletteGrid
from scripts.Helper.Resources import *

"""
Widget to create a colormap button
"""
class ColorMapButton(QToolButton):
    colorMapSelected = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)

        self.noneIconGraphic = None
        self.colorMap = None

        self.initUI()

        self.popup.palette.selected.connect(self.colorMapUpdated)

    def initUI(self):
        self.popup = Action(self)
        self.addAction(self.popup)

        self.setPopupMode(QToolButton.InstantPopup)

        self.noneIconGraphic = QIcon(resource_path("icons/colormap.png"))
        self.setIcon(self.noneIconGraphic)

    def colorMapUpdated(self, colorMap):
        self.colorMap = colorMap
        self.colorMapSelected.emit(colorMap)


class Action(QWidgetAction):
    def __init__(self, parent):
        super().__init__(parent)

        self.cmapPicker = None
        self.lut = None
        self.palette = None

        self.initUI()

    def initUI(self):
        self.cmapPicker = ColorMapPicker()
        self.palette = self.cmapPicker._palette

        self.setDefaultWidget(self.cmapPicker)


class ColorMapPicker(QWidget):
    def __init__(self):
        super().__init__()

        self._palette = None
        self._cmap = None

        self.initUI()

        self._palette.selected.connect(self.setCMap)

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)

        self._palette = PaletteGrid('sequential', n_columns=4)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self._palette)
        self.centralLayout.setAlignment(Qt.AlignCenter)
        self.centralLayout.setContentsMargins(3, 3, 3, 3)

        self.setLayout(self.centralLayout)

    def setCMap(self, cmap):
        self._cmap = cmap
