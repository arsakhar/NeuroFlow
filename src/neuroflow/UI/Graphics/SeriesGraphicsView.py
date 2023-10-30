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

from .OverlayGraphics import OverlayGraphics
from ..Stats.ImageStats import ImageStats
from ...ToolBox.AutoSegmentation import AutoSegmentation
from ..Cursor import Cursor
from ...Helper.SegmentationRegion import SegmentationRegion


class SeriesGraphicsView(PGImageView):
    """
    Custom QGraphicsView for displaying series images and handling overlays and segmentations.

    This class inherits from PGImageView and extends its functionality to handle overlays and segmentations.

    Attributes
    ----------
    newSegmentationBundle : pyqtSignal
       Signal emitted when a new segmentation bundle is generated.

    Parameters
    ----------
    parent : QObject
       The parent QObject for this graphics view.

    toolBar : ToolBar
       The toolbar object associated with the graphics view.

    """

    newSegmentationBundle = pyqtSignal(object)

    def __init__(self, parent, toolBar):
        """
        Initializes the SeriesGraphicsView object.

        Parameters
        ----------
        parent : QObject
            The parent QObject for this graphics view.

        toolBar : ToolBar
            The toolbar object associated with the graphics view.

        """

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
        """
        Initializes the user interface components and layout.

        """

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

    def newPatient(self, patient):
        """
        Resets the view when a new patient is selected.

        Parameters
        ----------
        patient : object
            The selected patient object.

        """

        self.reset()

    def reset(self):
        """
        Resets the view to its initial state.

        """

        self.clear()
        self.view.setCursor(self.cursor.DefaultCursor)
        # self.imageStats.disable()
        self.imageItem.lut = self.toolBar.colorMapBtn.colorMap

    def setOverlayCursor(self, overlayColor):
        """
        Sets the cursor based on the presence of an overlay.

        Parameters
        ----------
        overlayColor : str, optional
            The color of the overlay, None if no overlay is present.

        """

        if overlayColor is None:
            self.view.setCursor(self.cursor.DefaultCursor)

        else:
            self.view.setCursor(self.cursor.CrossCursor)

    def setLookupTable(self, lut):
        """
        Sets the lookup table for the image.

        Parameters
        ----------
        lut : object
            The lookup table object to be set.

        """

        self.imageItem.setLookupTable(lut)

    def play(self, rate):
        """
        Plays the series images as a slideshow.

        Parameters
        ----------
        rate : int
            The rate at which images are displayed in milliseconds.

        """

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

    def timeout(self):
        """
        Handles the timeout event during the slideshow.

        """

        if self.currentIndex == (self.image.shape[0] - 1):
            self.playTimer.stop()
            self.toolBar.playBtn.setPlayState()

            return

        super().timeout()

    def seriesSelected(self, series):
        """
        Handles the selection of a new series.

        Parameters
        ----------
        series : object, optional
            The selected series object, None if no series is selected.

        """

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

    def newMask(self, mask):
        """
        Processes a new mask to generate a segmentation bundle.

        Parameters
        ----------
        mask : object
            The mask object containing segmented regions.

        """

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

    def timeLineChanged(self):
        """
        Handles changes in the timeline slider.

        """

        super().timeLineChanged()

    def setViewScale(self, imageScale):
        """
        Sets the scale and limits of the view based on the image dimensions.

        Parameters
        ----------
        imageScale : float
            The scale factor for the image.

        """

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

    def getImageScale(self, imageData):
        """
        Calculates the appropriate image scale based on the view dimensions.

        Parameters
        ----------
        imageData : np.ndarray
            The image data array.

        Returns
        -------
        float
            The calculated image scale factor.

        """

        viewWidth = self.view.screenGeometry().width()
        viewHeight = self.view.screenGeometry().height()

        if viewWidth < viewHeight:
            imageScale = viewWidth / imageData.shape[1]

        else:
            imageScale = viewHeight / imageData.shape[2]

        return imageScale


class SegmentationBundle:
    """
    Bundle class to store segmented regions.

    This class represents a collection of segmented regions. It provides a container to store multiple segmentation
    regions.

    Attributes
    ----------
    regions : list
        A list to store segmented regions.

    """

    def __init__(self):
        """
        Initialize an empty SegmentationBundle object.

        """

        self.regions = []


class ViewBox(pg.ViewBox):
    """
    Custom view box for displaying interactive graphical data.

    This class extends the functionality of pg.ViewBox to provide additional mouse interactions and cursor changes.

    """

    def __init__(self):
        """
        Initialize the ViewBox.

        """

        super().__init__()

        self.cursor = Cursor()

        self.initUI()

    def initUI(self):
        """
        Initialize the user interface settings for the ViewBox.

        """

        self.setAspectLocked(True)
        self.setMouseMode(pg.ViewBox.PanMode)

    def mouseDragEvent(self, ev, axis=None):
        """
        Handle mouse drag events over the view box.

        Parameters
        ----------
        ev : MouseDragEvent
            The mouse drag event.

        axis : int, optional
            The axis along which the drag event occurs. Default is None.

        """

        if ev.isStart():
            self.setCursor(self.cursor.ClosedHandCursor)

        if ev.isFinish():
            self.setCursor(self.cursor.DefaultCursor)

        super().mouseDragEvent(ev, axis)

    def mouseClickEvent(self, ev):
        """
        Handle mouse click events over the view box.

        Parameters
        ----------
        ev : object
            The mouse click event.

        """

        if ev.button() == Qt.LeftButton:
            super().mouseClickEvent(ev)
        else:
            return

    def wheelEvent(self, ev, axis=None):
        """
        Handle wheel events over the view box.

        Parameters
        ----------
        ev : object
            The wheel event.

        axis : int, optional
            The axis along which the wheel event occurs. Default is None.

        """

        super().wheelEvent(ev, axis)

    def resizeEvent(self, ev):
        """
        Handle resize events for the view box.

        Parameters
        ----------
        ev : object
            The resize event.

        """

        super().resizeEvent(ev)


class ImageItem(pg.ImageItem):
    """
    Custom image item for displaying images with additional signals and interactions.

    This class extends the functionality of pg.ImageItem to provide additional signals and interactions.

    Attributes
    ----------
    leftMouseDragged : pyqtSignal
        Signal emitted when the left mouse button is dragged over the image.

    mouseHovered : pyqtSignal
        Signal emitted when the mouse hovers over the image.

    contextMenuTriggered : pyqtSignal
        Signal emitted when the context menu is triggered over the image.

    """

    leftMouseDragged = pyqtSignal(mouseEvents.MouseDragEvent)
    mouseHovered = pyqtSignal(mouseEvents.HoverEvent)
    contextMenuTriggered = pyqtSignal(object)

    def __init__(self, toolBar):
        """
        Initialize the ImageItem with the specified toolbar.

        Parameters
        ----------
        toolBar : ToolBar
            The toolbar associated with the ImageItem.

        """

        super().__init__()

        self.toolBar = toolBar
        self.image = np.zeros((toolBar.width(), toolBar.height(), 3))

    def mouseDragEvent(self, ev, axis=None):
        """
        Handle mouse drag events over the image.

        Parameters
        ----------
        ev : MouseDragEvent
            The mouse drag event.

        axis : int, optional
            The axis along which the drag event occurs. Default is None.

        """

        if self.toolBar.overlayBtn.overlayColor is None:
            super().mouseDragEvent(ev)

            return

        if ev.button() == Qt.LeftButton:
            self.leftMouseDragged.emit(ev)

    def hoverEvent(self, ev):
        """
        Handle mouse hover events over the image.

        Parameters
        ----------
        ev : HoverEvent
            The hover event.

        """

        if self.toolBar.overlayBtn.overlayColor is None:
            super().hoverEvent(ev)

            self.mouseHovered.emit(ev)

            return

        self.mouseHovered.emit(ev)
        ev.acceptDrags(QtCore.Qt.LeftButton)

    def contextMenuEvent(self, event):
        """
        Handle context menu events over the image.

        Parameters
        ----------
        event : object
            The context menu event.

        """

        self.contextMenuTriggered.emit(event)
