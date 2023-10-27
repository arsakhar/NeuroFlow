from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon

from ...Helper.Resources import *

"""
Widget to create play button
"""
class PlayButton(QToolButton):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setToolTip("Play Image")
        self.setPlayState()

    def setPauseState(self):
        self.setIcon(QIcon(resource_path('icons/24x24/cil-media-pause.png')))

    def setPlayState(self):
        self.setIcon(QIcon(resource_path('icons/24x24/cil-media-play.png')))
