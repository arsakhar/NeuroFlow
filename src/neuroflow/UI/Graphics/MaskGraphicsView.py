import numpy as np
import pyqtgraph as pg
from PIL import Image, ImageDraw
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout
from pyqtgraph import GraphicsView as PGGraphicsView
from pyqtgraph.GraphicsScene import mouseEvents

from ...Helper.SegmentationRegion import SegmentationRegion
from ...UI.Cursor import Cursor
from ...UI.Graphics.KernelGraphics import KernelGraphics


class MaskGraphicsView(PGGraphicsView):
    """
    Custom graphics view for interactive masking operations.

    This class extends the functionality of PGGraphicsView to provide interactive masking features.

    Attributes
    ----------
    newMask : pyqtSignal
       Signal emitted when a new mask is created or modified.

    """

    newMask = pyqtSignal(object)

    def __init__(self, parent, toolBar):
        """
        Initialize the MaskGraphicsView with the specified parent and toolbar.

        Parameters
        ----------
        parent : QWidget
            The parent widget containing the MaskGraphicsView.

        toolBar : ToolBar
            The toolbar widget associated with the MaskGraphicsView.

        """

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
        """
        Initialize the user interface of the MaskGraphicsView.

        """

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

    def newPatient(self, patient):
        """
        Handle a new patient being selected.

        Parameters
        ----------
        patient : Patient
            The selected patient object.

        """

        self.reset()

    def reset(self):
        """
        Reset the mask and cursor to default states.

        """

        self.maskItem.clear()
        self.setCursor(self.cursor.DefaultCursor)

    def clear(self):
        """
        Clear the current mask.

        """

        if self.maskItem.image is not None:
            self.maskItem.image[:, :] = 0
            self.maskItem.updateImage()

    def seriesSelected(self, series):
        """
        Handle selection of a new series.

        Parameters
        ----------
        series : Series
            The selected series object.

        """

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

    def newStamp(self, mask):
        """
        Handle a new mask stamp being created.

        Parameters
        ----------
        mask : np.ndarray
            The mask stamp.

        """

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

    def newOverlay(self, overlay):
        """
        Apply a new mask overlay on the current mask.

        Parameters
        ----------
        overlay : Overlay
            The overlay object containing regions to be applied on the mask.

        """

        self.view.removeItem(self.maskItem)

        imageShape = (self.maskItem.image.shape[0], self.maskItem.image.shape[1])

        overallMask = np.empty(imageShape)

        self.mask = Mask()

        for region in overlay.regions:
            regionCoordinates = [(coordinate.x(), coordinate.y()) for coordinate in region.vertices]
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

    def newAutoSeg(self, vertices):
        """
        Apply a new auto-segmentation on the current mask.

        Parameters
        ----------
        vertices : list of tuple
            List of (x, y) coordinates representing the vertices of the auto-segmentation polygon.

        """

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
    """
    Represents a mask containing regions of interest.

    This class defines a mask object that contains a list of regions of interest (ROIs).

    Attributes
    ----------
    regions : list
        A list to store the regions of interest in the mask.

    """

    def __init__(self):
        """
        Initializes an empty mask with no regions.

        """

        self.regions = []


class ViewBox(pg.ViewBox):
    """
    Custom ViewBox for interactive plotting.

    This class extends the functionality of the pg.ViewBox by providing custom mouse event handling.

    Attributes
    ----------
    graphicsWidget : QGraphicsWidget
        Parent graphics widget associated with the ViewBox.

    """

    def __init__(self, parent):
        super().__init__()

        self.cursor = Cursor()

        self.graphicsWidget = parent

    def initUI(self):
        self.setMouseEnabled(True)

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
        if ev.button() == Qt.RightButton:
            return


class MaskItem(pg.ImageItem):
    """
    Custom ImageItem for displaying and interacting with masked images in a PlotWidget.

    This class extends the functionality of the pg.ImageItem by providing signals for left mouse press and drag events.

    Attributes
    ----------
    leftMousePressed : pyqtSignal
       Signal emitted when a left mouse button is pressed on the MaskItem.

    leftMouseDragged : pyqtSignal
       Signal emitted when the left mouse button is dragged on the MaskItem.

    """

    leftMousePressed = pyqtSignal(mouseEvents.MouseClickEvent)
    leftMouseDragged = pyqtSignal(mouseEvents.MouseDragEvent)

    def __init__(self, image=None):
        """
        Initialize the MaskItem with the specified image.

        Parameters
        ----------
        image : QImage, optional
            The image to be displayed in the MaskItem.

        """

        super().__init__(image=image)

    def mouseClickEvent(self, ev):
        """
        Handle mouse click events on the MaskItem.

        Parameters
        ----------
        ev : QGraphicsSceneMouseEvent
            The mouse event object containing information about the click event.

        """

        if ev.button() == Qt.RightButton:
            return

        if ev.button() == Qt.LeftButton:
            self.leftMousePressed.emit(ev)

    def mouseDragEvent(self, ev):
        """
        Handle mouse drag events on the MaskItem.

        Parameters
        ----------
        ev : QGraphicsSceneMouseEvent
            The mouse event object containing information about the drag event.

        """

        if ev.button() != Qt.LeftButton:
            return
        else:
            self.leftMouseDragged.emit(ev)

    def updateImage(self, *args, **kargs):
        """
        Update the image displayed in the MaskItem.

        Parameters
        ----------
        *args, **kargs
            Additional arguments to update the image.

        """

        super().updateImage(*args, **kargs)


class GridItem(pg.GridItem):
    """
    Custom grid item for a PlotWidget.

    This class extends the functionality of the pg.GridItem by allowing customization of the text pen.

    Parameters
    ----------
    textPen : QColor or None, optional
        Pen color for the grid text. If None, the default color is used.

    """

    def __init__(self, textPen =None):
        """
        Initialize the GridItem with the specified text pen color.

        Parameters
        ----------
        textPen : QColor or None, optional
            Pen color for the grid text. If None, the default color is used.

        """

        super().__init__(textPen=textPen)
