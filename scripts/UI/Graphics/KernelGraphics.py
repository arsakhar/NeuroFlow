from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import pyqtSignal
from pyqtgraph.GraphicsScene import mouseEvents
import numpy as np
import math
from scripts.UI.Cursor import Cursor


class KernelGraphics(QGraphicsObject):
    newStamp = pyqtSignal(object)

    def __init__(self, maskView, maskItem, toolBar):
        super().__init__()
        self.maskView = maskView
        self.maskItem = maskItem

        self.toolBar = toolBar
        self.setSize(self.toolBar.kernelBtn.kernelSize)
        self.toolBar.kernelBtn.kernelSelected.connect(self.setSize)

        self.eraseMode = False

        self.enabled = False

    def subscribe(self):
        self.unsubscribe()

        self.maskItem.leftMousePressed.connect(self.stampOnMouseAction)
        self.maskItem.leftMouseDragged.connect(self.stampOnMouseAction)

    def unsubscribe(self):
        try:
            self.maskItem.leftMousePressed.disconnect(self.stampOnMouseAction)
        except:
            pass

        try:
            self.maskItem.leftMouseDragged.disconnect(self.stampOnMouseAction)
        except:
            pass

    """
    Sets the size of the draw kernel.
    ================== ===========================================================================
    **Arguments:**
    kernelSize         a 2d numpy array of 1's. size is defined by arrays shape
    ================== ===========================================================================
    """
    def setSize(self, kernelSize):
        cursor = Cursor()

        if kernelSize is None:
            self.maskView.graphicsWidget.setCursor(cursor.DefaultCursor)
            self.enabled = False

            return

        self.kernelSize = kernelSize

        self.kernel = np.tile(np.ones(self.kernelSize), (self.kernelSize, 1))
        self.maskItem.setDrawKernel(kernel=self.kernel,
                                    center=(math.floor(self.kernelSize / 2), math.floor(self.kernelSize / 2)),
                                    mode='set')

        self.maskView.graphicsWidget.setCursor(cursor.CrossCursor)

        self.enabled = True

    """
    Adds kernel at the current mouse position if mask is empty. Otherwise, erases existing kernel.
    ================== ===========================================================================
    **Arguments:**
    ev                 mouse event
    ================== ===========================================================================
    """
    def stampOnMouseAction(self, ev):
        if not self.enabled:
            return

        itemPos = ev.pos()
        viewPos = self.maskView.mapFromItemToView(self.maskItem, itemPos)

        i, j = viewPos.x(), viewPos.y()

        i = int(np.clip(i, 0, self.maskItem.image.shape[0] - 1))
        j = int(np.clip(j, 0, self.maskItem.image.shape[1] - 1))
        val = self.maskItem.image[i, j]

        bound_1 = math.floor(self.kernel.shape[0] / 2)
        bound_2 = math.ceil(self.kernel.shape[0] / 2)

        if type(ev) == mouseEvents.MouseDragEvent:
            if ev.isStart():
                if val == 1:
                    self.eraseMode = True
                else:
                    self.eraseMode = False

            if ev.isFinish():
                self.newStamp.emit(self.maskItem.image)

            if self.eraseMode:
                self.maskItem.image[(i - bound_1):(i + bound_2), (j - bound_1):(j + bound_2)] = 0
            else:
                self.maskItem.drawAt(viewPos, ev)

        elif type(ev) == mouseEvents.MouseClickEvent:
            if val == 1:
                self.maskItem.image[(i - bound_1):(i + bound_2), (j - bound_1):(j + bound_2)] = 0
            else:
                self.maskItem.drawAt(viewPos, ev)

            self.newStamp.emit(self.maskItem.image)

        self.maskItem.updateImage()
