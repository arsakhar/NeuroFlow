from PyQt5.QtWidgets import QGraphicsObject
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from skimage.segmentation import active_contour
from skimage.filters import gaussian
import numpy as np
import itertools


"""
Widget used to draw overlays on image. Must use same viewbox as image widget.
"""
class AutoSegmentation(QGraphicsObject):
    newAutoSeg = pyqtSignal(object)

    def __init__(self, seriesGraphics, toolBar):
        super().__init__()
        self.seriesGraphics = seriesGraphics
        self.viewBox = seriesGraphics.view
        self.imageItem = seriesGraphics.imageItem

        self.toolBar = toolBar
        self.toolBar.autoSegBtn.autoSegSelected.connect(self.runAutoSeg)

    """
    Runs auto segmentation routine
    """
    def runAutoSeg(self, autoSegBtn):
        if autoSegBtn == self.toolBar.autoSegBtn.activeContourBtn:
            self.runActiveContour()

    """
    Use the active contour algorithm to fit a closed spline to the edge of an ROI
    https://scikit-image.org/docs/dev/auto_examples/edges/plot_active_contours.html
    """
    def runActiveContour(self):
        # find minimum and maximum view coordinates in x-direction
        minX = self.viewBox.viewRange()[0][0]
        maxX = self.viewBox.viewRange()[0][1]

        # find minimum and maximum view coordinates in y-direction
        minY = self.viewBox.viewRange()[1][0]
        maxY = self.viewBox.viewRange()[1][1]

        # group coordinates into 4-corner boundaries
        topLeft = QtCore.QPointF(minX, minY)
        topRight = QtCore.QPointF(maxX, minY)
        bottomLeft = QtCore.QPointF(minX, maxY)
        bottomRight = QtCore.QPointF(maxX, maxY)

        # convert view coordinates to item coordinates
        topLeft = self.viewBox.mapFromViewToItem(self.imageItem, topLeft)
        topRight = self.viewBox.mapFromViewToItem(self.imageItem, topRight)
        bottomLeft = self.viewBox.mapFromViewToItem(self.imageItem, bottomLeft)
        bottomRight = self.viewBox.mapFromViewToItem(self.imageItem, bottomRight)

        # round coordinates into whole numbers and determine row and column bounds
        rowBounds = (int(round(topLeft.y())), int(round(bottomLeft.y())))
        colBounds = (int(round(topLeft.x())), int(round(topRight.x())))

        # create an elliptical search area with the major and minor axis matching row/col bounds
        s = np.linspace(0, 2 * np.pi, 400)

        rCenter = (rowBounds[0] + rowBounds[1]) / 2
        cCenter = (colBounds[0] + colBounds[1]) / 2
        r = rCenter + (rowBounds[1] - rCenter) * np.sin(s)
        c = cCenter + (colBounds[1] - cCenter) * np.cos(s)

        # create search area array
        init = np.array([r, c]).T

        # transpose because active contour expects column-major (col, row) order? not sure why we do this actually
        image = self.seriesGraphics.image[self.seriesGraphics.currentIndex, :, :].T

        # use the active contour algorithm to identify roi.
        # https://scikit-image.org/docs/dev/auto_examples/edges/plot_active_contours.html
        snake = active_contour(image=gaussian(image, 3),
                               snake=init, alpha=0.015, beta=10, gamma=0.001, coordinates='rc')

        # convert snake coordinates to whole numbers (let's round up and down to create maximum possible boundary area)
        snake_floor = [[np.floor(i) for i in nested] for nested in snake]
        snake_ceil = [[np.ceil(i) for i in nested] for nested in snake]

        snake = snake_floor + snake_ceil

        # remove duplicate coordinates
        snake.sort()
        snake = list(vertice for vertice, _ in itertools.groupby(snake))

        self.newAutoSeg.emit(snake)
