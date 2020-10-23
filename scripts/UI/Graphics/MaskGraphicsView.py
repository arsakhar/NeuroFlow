from PyQt5.QtCore import pyqtSignal, Qt
import pyqtgraph as pg
from pyqtgraph import GraphicsView as PGGraphicsView
from pyqtgraph.GraphicsScene import mouseEvents
import numpy as np
from PIL import Image, ImageDraw
from PyQt5.QtWidgets import QFrame, QHBoxLayout

from scripts.UI.Graphics.KernelGraphics import KernelGraphics
from scripts.UI.Cursor import Cursor
from scripts.Helper.SegmentationRegion import SegmentationRegion


"""
Widget displays mask associated with overlay drawn on series graphics
"""
class MaskGraphicsView(PGGraphicsView):
    newMask = pyqtSignal(object)

    def __init__(self, parent, toolBar):
        super().__init__(parent)
        self.view = ViewBox(self)

        self.toolBar = toolBar
        self.toolBar.clearBtn.clicked.connect(self.clear)

        self.cursor = Cursor()

        self.gridItem = GridItem(textPen=None)
        self.gridItem.setZValue(10)
        self.view.addItem(self.gridItem)

        self.maskItem = MaskItem()
        self.view.addItem(self.maskItem)

        self.kernelGraphics = KernelGraphics(self.view, self.maskItem, self.toolBar)
        self.kernelGraphics.newStamp.connect(self.newStamp)

        self.mask = None

        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.setObjectName("maskView")
        self.view.invertY()
        self.view.setAspectLocked(True)
        self.setCentralItem(self.view)
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.centralFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)

        self.show()

    """
    Called when new patient is loaded. Calls reset function
    ================== ===========================================================================
    **Arguments:**
    patient            loaded patient
    ================== ===========================================================================
    """
    def newPatient(self, patient):
        self.reset()

    """
    Clears mask item and sets image to None
    """
    def reset(self):
        self.maskItem.clear()
        self.setCursor(self.cursor.DefaultCursor)

    """
    Resets binary mask array in mask item to all 0's
    """
    def clear(self):
        if self.maskItem.image is not None:
            self.maskItem.image[:, :] = 0
            self.maskItem.updateImage()

    """
    Clears the existing mask. Called when the active series has changed.
    ================== ===========================================================================
    **Arguments:**
    series             the series object
    ================== ===========================================================================
    """
    def seriesSelected(self, series):
        self.reset()

        if series is None:
            self.kernelGraphics.unsubscribe()

            return

        elif series.parentSequence.getSeriesByType("Phase") is None:
            self.kernelGraphics.unsubscribe()

            return

        images = []

        for image in series.images:
            images.append(image.pixel_array.T)

        images = np.array(images)

        mask = np.zeros((images.shape[1], images.shape[2]))

        self.maskItem.setImage(mask)
        self.view.addItem(self.maskItem)
        self.maskItem.updateImage()

        self.kernelGraphics.subscribe()

    """
    Called when the kernel stamper changes the existing mask.
    ================== ===========================================================================
    **Arguments:**
    mask               numpy array mask
    
    **Signal:**
    newMask            returns mask object
    ================== ===========================================================================
    """
    def newStamp(self, mask):
        self.mask = Mask()

        # adjust emitted mask
        adjustedMask = np.copy(mask)
        non_zero_indexes = np.nonzero(adjustedMask)
        nonzero_row = non_zero_indexes[0]
        nonzero_col = non_zero_indexes[1]

        for row, col in zip(nonzero_row, nonzero_col):
            if adjustedMask[row + 1, col] == 0:
                adjustedMask[row + 1, col] = 1

            if adjustedMask[row, col + 1] == 0:
                adjustedMask[row, col + 1] = 1

            if adjustedMask[row + 1, col + 1] == 0:
                adjustedMask[row + 1, col + 1] = 1

        _region = SegmentationRegion()
        _region.mask = adjustedMask

        self.mask.regions.append(_region)

        self.newMask.emit(self.mask)

    """
    Updates the mask to match the overlay. Overlay is assumed to be in image item coordinates.
    ================== ===========================================================================
    **Arguments:**
    overlay            overlay object containing all independent overlays
    ================== ===========================================================================
    """
    def newOverlay(self, overlay):
        self.view.removeItem(self.maskItem)

        imageShape = (self.maskItem.image.shape[0], self.maskItem.image.shape[1])

        overallMask = np.empty(imageShape)

        self.mask = Mask()

        for region in overlay.regions:
            regionVertices = region.vertices

            regionCoordinates = [tuple([vertice.x(), vertice.y()]) for vertice in regionVertices]
            regionMask = Image.new('L', imageShape)

            ImageDraw.Draw(regionMask).polygon(regionCoordinates, outline=1, fill=1)

            regionMask = np.array(regionMask).T

            # adjust displayed mask to match overlay
            adjustedMask = np.copy(regionMask)
            non_zero_indexes = np.nonzero(adjustedMask)
            nonzero_row = non_zero_indexes[0]
            nonzero_col = non_zero_indexes[1]

            for row, col in zip(nonzero_row, nonzero_col):
                if adjustedMask[row + 1, col] == 0:
                    adjustedMask[row, col] = 0

                if adjustedMask[row, col + 1] == 0:
                    adjustedMask[row, col] = 0

                if adjustedMask[row + 1, col + 1] == 0:
                    adjustedMask[row, col] = 0

            overallMask = adjustedMask + overallMask

            region.mask = regionMask
            self.mask.regions.append(region)

        overallMask[overallMask > 1] = 0

        self.maskItem.setImage(overallMask)
        self.view.addItem(self.maskItem)
        self.maskItem.updateImage()

        self.newMask.emit(self.mask)

    """
    Updates the mask to match the overlay. Overlay is assumed to be in image item coordinates.
    ================== ===========================================================================
    **Arguments:**
    vertices           A list of tuples containing vertices from autosegmentation routine
    ================== ===========================================================================
    """
    def newAutoSeg(self, vertices):
        self.view.removeItem(self.maskItem)

        imageShape = (self.maskItem.image.shape[0], self.maskItem.image.shape[1])

        self.mask = Mask()

        overallMask = np.empty(imageShape)

        autoSegCoordinates = [tuple(vertice) for vertice in vertices]

        autoSegMask = Image.new('L', imageShape)
        ImageDraw.Draw(autoSegMask).polygon(autoSegCoordinates, outline=1, fill=1)
        autoSegMask = np.array(autoSegMask)

        overallMask = autoSegMask + overallMask

        overallMask[overallMask > 1] = 0

        _region = SegmentationRegion()
        _region.mask = overallMask
        self.mask.regions.append(_region)

        self.maskItem.setImage(overallMask)
        self.view.addItem(self.maskItem)
        self.maskItem.updateImage()

        self.newMask.emit(self.mask)


class Mask:
    def __init__(self):
        self.regions = []


"""
The pyqtgraph viewbox. The viewbox displays items.
"""
class ViewBox(pg.ViewBox):
    def __init__(self, parent):
        super().__init__()

        self.graphicsWidget = parent

    def initUI(self):
        self.setMouseEnabled(True)

    def mouseDragEvent(self, ev, axis=None):
        return

    def mouseClickEvent(self, ev):
        if ev.button() == Qt.RightButton:
            return


"""
The pyqtgraph image item. An image item stores the images.
"""
class MaskItem(pg.ImageItem):
    leftMousePressed = pyqtSignal(mouseEvents.MouseClickEvent)
    leftMouseDragged = pyqtSignal(mouseEvents.MouseDragEvent)

    def __init__(self, image=None):
        super().__init__(image=image)

    def mouseClickEvent(self, ev):
        if ev.button() == Qt.RightButton:
            return

        if ev.button() == Qt.LeftButton:
            self.leftMousePressed.emit(ev)

    def mouseDragEvent(self, ev):
        if ev.button() != Qt.LeftButton:
            return
        else:
            self.leftMouseDragged.emit(ev)

    def updateImage(self, *args, **kargs):
        super().updateImage(*args, **kargs)


"""
The pyqtgraph grid item. A grid item displays grid lines
"""
class GridItem(pg.GridItem):
    def __init__(self, textPen=None):
        super().__init__(textPen=textPen)
