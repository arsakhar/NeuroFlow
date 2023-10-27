from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal as Signal
from matplotlib import cm
import numpy as np

from Resources import *

PALETTES = {
    'sequential': [['CMRmap', 'icons/colormaps/cmrmap.png'], ['Default', 'icons/colormaps/default.png']]
}


class _PaletteButton(QtWidgets.QPushButton):
    def __init__(self, colorMap):
        super().__init__()
        self.setFixedSize(QtCore.QSize(24, 24))
        self.colorMap = self.getlut(colorMap[0])
        hoverStylesheet = "QPushButton:hover { background-color: rgb(85, 170, 255); }"
        self.setStyleSheet(hoverStylesheet)
        self.setIcon(QIcon(resource_path(colorMap[1])))
        self.setCheckable(True)

    def getlut(self, cmap):
        if cmap == "Default":
            return None

        colormap = cm.get_cmap(cmap)
        colormap._init()
        lut = (colormap._lut * 255).view(np.ndarray)

        return lut

class _PaletteBase(QtWidgets.QWidget):
    selected = Signal(object)

    def _emit_colorMap(self, color):
        self.selected.emit(color)


class _PaletteLinearBase(_PaletteBase):
    def __init__(self, colorMaps, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(colorMaps, str):
            if colorMaps in PALETTES:
                colorMaps = PALETTES[colorMaps]

        palette = self.layoutvh()

        for c in colorMaps:
            b = _PaletteButton(c)
            b.pressed.connect(
                lambda c=c: self._emit_colorMap(c)
            )
            palette.addWidget(b)

        self.setLayout(palette)


class PaletteHorizontal(_PaletteLinearBase):
    layoutvh = QtWidgets.QHBoxLayout


class PaletteVertical(_PaletteLinearBase):
    layoutvh = QtWidgets.QVBoxLayout


class PaletteGrid(_PaletteBase):
    def __init__(self, colorMaps, n_columns=5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(colorMaps, str):
            if colorMaps in PALETTES:
                colorMaps = PALETTES[colorMaps]

        palette = QtWidgets.QGridLayout()
        row, col = 0, 0

        for c in colorMaps:
            b = _PaletteButton(c)
            b.setChecked(True)
            b.pressed.connect(
                lambda b=b: self.buttonPressed(b)
            )

            palette.addWidget(b, row, col)
            col += 1
            if col == n_columns:
                col = 0
                row += 1

        self.setLayout(palette)

    def buttonPressed(self, button):
        if button.isChecked():
            self._emit_colorMap(button.colorMap)
        else:
            self._emit_colorMap(None)
