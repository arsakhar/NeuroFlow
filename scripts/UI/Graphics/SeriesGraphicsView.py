from pyqtgraph import ImageView as PGImageView
import numpy as np
import math
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import pyqtgraph as pg
from pyqtgraph.GraphicsScene import mouseEvents
from PyQt5.QtWidgets import QFrame, QHBoxLayout
from itertools import groupby

from scripts.UI.Graphics.OverlayGraphics import OverlayGraphics
from scripts.UI.Stats.ImageStats import ImageStats
from scripts.ToolBox.AutoSegmentation import AutoSegmentation
from scripts.UI.Cursor import Cursor
from scripts.Helper.SegmentationRegion import SegmentationRegion


"""
Widget that takes a viewbox and image item to display images associated with Series
"""
class SeriesGraphicsView(PGImageView):
    newSegmentationBundle = pyqtSignal(object)

    def __init__(self, parent, toolBar):
        super().__init__(parent=parent, view=ViewBox(), imageItem=ImageItem(toolBar))

        self.toolBar = toolBar
        self.toolBar.playBtn.clicked.connect(lambda x: self.play(5))
        self.toolBar.colorMapBtn.colorMapSelected.connect(self.setLookupTable)
        self.toolBar.overlayBtn.overlaySelected.connect(self.setOverlayCursor)

        self.cursor = Cursor()

        self.overlay = OverlayGraphics(self.view, self.imageItem, self.toolBar)
        self.autoSeg = AutoSegmentation(self, self.toolBar)
        self.imageStats = ImageStats(self)

        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.setMinimumWidth(500)
        self.setMinimumHeight(300)
        self.setObjectName("imageView")
        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.ui.roiPlot.setVisible(False)
        self.ignorePlay = False
        self.ui.splitter.setSizes([self.height() - 35, 35])

        self.splitterHandle = self.ui.splitter.handle(1)
        self.splitterHandle.setEnabled(False)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.centralFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)

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
    Clears image item and sets image to None
    """
    def reset(self):
        self.clear()
        self.view.setCursor(self.cursor.DefaultCursor)
        # self.imageStats.disable()
        self.imageItem.lut = self.toolBar.colorMapBtn.colorMap

    """
    Sets cursor for series viewbox
    ================== ===========================================================================
    **Arguments:**
    activeOverlay      the overlay selected in the toolbar
    ================== ===========================================================================
    """
    def setOverlayCursor(self, overlayColor):
        if overlayColor is None:
            self.view.setCursor(self.cursor.DefaultCursor)

        else:
            self.view.setCursor(self.cursor.CrossCursor)

    """
    Sets color map for series images
    ================== ===========================================================================
    **Arguments:**
    lut                lookup table
    ================== ===========================================================================
    """
    def setLookupTable(self, lut):
        self.imageItem.setLookupTable(lut)

    """
    Iterates through the image slices at specified rate
    ================== ===========================================================================
    **Arguments:**
    rate               play rate
    ================== ===========================================================================
    """
    def play(self, rate):
        if self.ignorePlay:
            return

        if self.playTimer.isActive():
            self.playTimer.stop()
            self.toolBar.playBtn.setPlayState()

            return

        if self.currentIndex == (self.image.shape[0] - 1):
            self.setCurrentIndex(0)

        self.toolBar.playBtn.setPauseState()

        super().play(rate)

    """
    Checks for completion of play
    """
    def timeout(self):
        if self.currentIndex == (self.image.shape[0] - 1):
            self.playTimer.stop()
            self.toolBar.playBtn.setPlayState()

            return

        super().timeout()

    """
    Displays the images associated with the active series.
    ================== ===========================================================================
    **Arguments:**
    series             the series object
    ================== ===========================================================================
    """
    def seriesSelected(self, series):
        self.reset()

        if series is None:
            return

        images = []

        for image in series.images:
            images.append(image.pixel_array)

        imageData = np.array(images)

        # pytgraph assumes images are in column-major order (col, row) so we need to transpose data into that format
        imageData = imageData.transpose((0, 2, 1))

        # scaling the image to fit the viewbox dimensions is causing all sorts of issues. set to 1 for now
        imageScale = 1
        # imageScale = self.getImageScale(imageData)

        # set image for imageView
        self.setImage(imageData, scale=(imageScale, imageScale))

        self.setViewScale(imageScale)  # adjust view to fit new image
        self.view.addItem(self.imageItem)

        # show image stats panel
        # self.imageStats.enable()

        self.toolBar.colorMapBtn.colorMap = self.imageItem.lut

    """
    Updates the imageROI to match the image region specified by the mask. Mask is assumed to be
    in mask item coordinates.
    ================== ===========================================================================
    **Arguments:**
    mask               the mask
    ================== ===========================================================================
    """
    def newMask(self, mask):
        self.segmentationBundle = SegmentationBundle()

        regions = mask.regions

        regionsSorted = sorted(regions, key=lambda x: x.id)
        regionsGroupedBy = groupby(regionsSorted, key=lambda x: x.id)

        regionsGrouped = {}
        for _id, _regions in regionsGroupedBy:
            regionsGrouped[_id] = list(_regions)

        for _id, _regions in regionsGrouped.items():
            mask = sum(region.mask for region in _regions)

            mask[mask > 1] = 0

            maskCoordinates = np.argwhere(mask)
            maskCoordinates = [QtCore.QPointF(coordinate[0], coordinate[1]) for coordinate in maskCoordinates]

            maskCoordinates = [[math.floor(coordinate.x()), math.floor(coordinate.y())] for coordinate in
                               maskCoordinates]

            mask = np.zeros((self.image.shape[1], self.image.shape[2]))

            x_coords = [c[0] for c in maskCoordinates]
            y_coords = [c[1] for c in maskCoordinates]

            mask[x_coords, y_coords] = 1

            mask[mask == 0] = np.nan  # convert mask zeros to nan to differentiate between image zeros

            mask = np.ma.masked_invalid(mask)  # create a mask array to handle nan during multiplication

            masked_image = mask * self.image  # multiply masked array by image

            masked_image = masked_image.filled(
                np.nan)  # convert back to numpy array, filling in masked values with nan

            masked_image = masked_image.transpose((0, 2, 1))  # transpose image back to row-major order (row, col)

            region = SegmentationRegion()
            region.image = masked_image
            region.id = _id

            self.segmentationBundle.regions.append(region)

        self.newSegmentationBundle.emit(self.segmentationBundle)

    """
    Changes the overlaid text based on the current image
    """
    def timeLineChanged(self):
        super().timeLineChanged()

    """
    Adjusts the view limits based on the image to display. Prevents zooming out too far.
    Centers image within the view.
    ================== ===========================================================================
    **Arguments:**
    imageScale         the scale of the image
    ================== ===========================================================================
    """
    def setViewScale(self, imageScale):
        self.view.setLimits(xMin=0,
                            xMax=self.imageItem.width() * imageScale,
                            yMin=0,
                            yMax=self.imageItem.height() * imageScale,
                            minXRange=1,
                            minYRange=1)

        # viewWidth = self.view.screenGeometry().width()
        # viewHeight = self.view.screenGeometry().height()

        # if viewWidth > viewHeight:
        #     self.view.setLimits(xMin=-(viewWidth - self.imageItem.width() * imageScale),
        #                         xMax=viewWidth,
        #                         yMin=0,
        #                         yMax=viewHeight,
        #                         minXRange=1,
        #                         minYRange=1)
        #
        # else:
        #     self.view.setLimits(xMin=0,
        #                         xMax=viewWidth,
        #                         yMin=-(viewHeight - self.imageItem.height() * imageScale),
        #                         yMax=viewHeight,
        #                         minXRange=1,
        #                         minYRange=1)

        self.view.translateBy(x=0, y=0)

        aspectRatio = self.image.shape[1] / self.image.shape[2]  # width / height ratio
        self.view.setAspectLocked(lock=True, ratio=aspectRatio)

    """
    Determines the proper image scale based on the viewbox.
    ================== ===========================================================================
    **Arguments:**
    imageData          the ndarray associated with the image
    
    **Returns:**
    imageScale         the image scale
    ================== ===========================================================================
    """
    def getImageScale(self, imageData):
        viewWidth = self.view.screenGeometry().width()
        viewHeight = self.view.screenGeometry().height()

        if viewWidth < viewHeight:
            imageScale = viewWidth / imageData.shape[1]

        else:
            imageScale = viewHeight / imageData.shape[2]

        return imageScale


class SegmentationBundle:
    def __init__(self):
        self.regions = []


"""
The pyqtgraph viewbox. The viewbox displays items.
"""
class ViewBox(pg.ViewBox):
    def __init__(self):
        super().__init__()

        self.cursor = Cursor()

        self.initUI()

    def initUI(self):
        self.setAspectLocked(True)
        self.setMouseMode(pg.ViewBox.PanMode)

    def mouseDragEvent(self, ev, axis=None):
        if ev.isStart():
            self.setCursor(self.cursor.ClosedHandCursor)

        if ev.isFinish():
            self.setCursor(self.cursor.DefaultCursor)

        super().mouseDragEvent(ev, axis)

    def mouseClickEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            super().mouseClickEvent(ev)
        else:
            return

    def wheelEvent(self, ev, axis=None):
        super().wheelEvent(ev, axis)

    def resizeEvent(self, ev):
        super().resizeEvent(ev)


"""
The pyqtgraph image item. An image item stores the images.
"""
class ImageItem(pg.ImageItem):
    leftMouseDragged = pyqtSignal(mouseEvents.MouseDragEvent)
    mouseHovered = pyqtSignal(mouseEvents.HoverEvent)
    contextMenuTriggered = pyqtSignal(object)

    def __init__(self, toolBar):
        super().__init__()

        self.toolBar = toolBar

    def mouseDragEvent(self, ev, axis=None):
        if self.toolBar.overlayBtn.overlayColor is None:
            super().mouseDragEvent(ev)

            return

        if ev.button() == Qt.LeftButton:
            self.leftMouseDragged.emit(ev)

    def hoverEvent(self, ev):
        if self.toolBar.overlayBtn.overlayColor is None:
            super().hoverEvent(ev)

            self.mouseHovered.emit(ev)

            return

        self.mouseHovered.emit(ev)
        ev.acceptDrags(QtCore.Qt.LeftButton)

    def contextMenuEvent(self, event):
        self.contextMenuTriggered.emit(event)
