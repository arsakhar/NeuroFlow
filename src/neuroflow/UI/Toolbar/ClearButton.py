from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon

from ...Helper.Resources import *

"""
Widget to create save button
"""
class ClearButton(QToolButton):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setToolTip("Clear Image and Mask")
        self.setIcon(QIcon(resource_path('icons/erase.png')))
