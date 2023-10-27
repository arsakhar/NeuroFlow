from PyQt5.QtWidgets import QToolButton, QWidgetAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal

from ...Helper.Resources import *

"""
Widget to create save button
"""
class AutoSegmentationButton(QToolButton):
    autoSegSelected = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)

        self.activeContourBtn = None
        self.nonIconGraphic = None

        self.initUI()

        self.activeContourBtn.triggered.connect(lambda x: self.autoSegTriggered(self.activeContourBtn))

    def initUI(self):
        self.activeContourBtn = Action(self)
        self.activeContourBtn.iconGraphic = QIcon(resource_path('icons/active-contour.png'))
        self.activeContourBtn.setIcon(self.activeContourBtn.iconGraphic)
        self.activeContourBtn.setText("Active Contour")

        self.setPopupMode(QToolButton.InstantPopup)

        self.addAction(self.activeContourBtn)

        self.setToolTip("Auto Segmentation")

        self.setStyleSheet(u"border: none")
        self.setContentsMargins(0, 0, 0, 0)

        self.noneIconGraphic = QIcon(resource_path('icons/auto-seg.png'))
        self.setIcon(self.noneIconGraphic)

    def autoSegTriggered(self, autoSegBtn):
        self.autoSegSelected.emit(autoSegBtn)


class Action(QWidgetAction):
    def __init__(self, parent):
        super().__init__(parent)
