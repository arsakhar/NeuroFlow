from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsObject, QMenu, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPen
import math
import numpy as np
import cv2

from src.neuroflow.Helper.SegmentationRegion import SegmentationRegion


"""
Widget used to draw overlays on image. Must use same viewbox as image widget.
"""
class OverlayGraphics(QGraphicsObject):
    newOverlay = pyqtSignal(object)
    updatedOverlay = pyqtSignal(object)

    def __init__(self, imageView, imageItem, toolBar):
        super().__init__()
        self.imageView = imageView
        self.imageItem = imageItem

        self.toolBar = toolBar

        self.roiPen = QtGui.QPen()
        self.roiPen.setWidthF(.1)
        self.roiPen.setStyle(QtCore.Qt.SolidLine)

        self.bgPen = QtGui.QPen()
        self.bgPen.setWidthF(.1)
        self.bgPen.setStyle(Qt.DotLine)

        self.overlay = Overlay()

        self.toolBar.overlayBtn.overlaySelected.connect(self.setOverlay)
        self.toolBar.clearBtn.clicked.connect(self.clear)

    def reset(self):
        self.unsubscribe()
        self.clear()
        self.enabled = False

    def newPatient(self, patient):
        self.reset()

    """
    Sets the color of the overlay pen.
    ================== ===========================================================================
    **Arguments:**
    overlayColor       hex color
    ================== ===========================================================================
    """
    def setOverlay(self, overlayColor):
        if overlayColor is None:
            self.enabled = False
            return

        self.enabled = True

        color = QColor(overlayColor)
        self.roiPen.setColor(color)

    """
    Clears all existing overlays. Called when the active series has changed.
    ================== ===========================================================================
    **Arguments:**
    series             the series object
    ================== ===========================================================================
    """
    def seriesSelected(self, series):
        self.reset()

        if series is None:
            return

        elif series.parentSequence.getSeriesByType("Phase") is None:
            return

        self.subscribe()

    """
    Enables overlay drawing by subscribing to the viewbox's left mouse drag signal 
    """
    def subscribe(self):
        self.imageItem.leftMouseDragged.connect(self.drawOnMouseDrag)
        self.imageItem.contextMenuTriggered.connect(self.checkROICollision)

    """
    Enables overlay drawing by subscribing to the viewbox's left mouse drag signal 
    """
    def unsubscribe(self):
        self.toolBar.overlayBtn.activeSeg = None

        try:
            self.imageItem.leftMouseDragged.disconnect(self.drawOnMouseDrag)
        except:
            pass

        try:
            self.imageItem.contextMenuTriggered.disconnect(self.checkROICollision)
        except:
            pass

    """
    Draws the overlay while the mouse is being dragged.
    ================== ===========================================================================
    **Arguments:**
    ev                 mouse event
    ================== ===========================================================================
    """
    def drawOnMouseDrag(self, ev):
        if not self.enabled:
            return

        currItemPos = ev.pos()

        # clamp item position to image vertices
        currItemPos = QtCore.QPointF(round(currItemPos.x()), round(currItemPos.y()))

        # get view position
        currViewPos = self.imageView.mapFromItemToView(self.imageItem, currItemPos)

        # if this is the first drag event, clear the regional vertices list
        if ev.isStart():
            self.prevItemPos = currItemPos

            self.region = SegmentationRegion()
            self.region.id = SegmentationRegion.DEFAULT
            self.region.color = self.roiPen.color()

            self.region.vertices.append(self.prevItemPos)

        # if this is the last drag event, close the overlay and clear the regional vertices list
        if ev.isFinish():
            # initialItemPos = self.imageView.mapFromViewToItem(self.imageItem, self.regionVertices[0])
            initialItemPos = self.region.vertices[0]

            self.interpolateSegments(currItemPos, prevItemPos=initialItemPos)

            self.overlay.regions.append(self.region)

            # let's emit our vertice groups in image item (coordinates)
            self.newOverlay.emit(self.overlay)

        # no point in adding redundant vertices
        if currItemPos == self.prevItemPos:
            return

        # no point in adding redundant vertices
        if self.imageView.mapFromItemToView(self.imageItem, currItemPos) in self.region.vertices[1:]:
            if self.imageView.mapFromItemToView(self.imageItem, self.prevItemPos) in self.region.vertices[:-1]:
                self.prevItemPos = currItemPos

                return

        # let's make sure the distance between consecutive mouse events equal to 1.
        # this indicates the consecutive mouse events are on the same axis (x or y) allowing
        # us to create a horizontal or vertical line segment. If the distance between events is not
        # equal to 1, it means means we'd need to draw a diagonal line. we'd rather have step-wise lines
        # as diagonal lines don't make sense because you can't create a kernel with a half-filled pixel
        distance = math.sqrt(
            (currItemPos.x() - self.prevItemPos.x()) ** 2 +
            (currItemPos.y() - self.prevItemPos.y()) ** 2)

        # if distance is not equal to 1, run subroutine to interpolate segments
        if distance != 1:
            self.interpolateSegments(currItemPos)

        else:
            prevViewPos = self.imageView.mapFromItemToView(self.imageItem, self.prevItemPos)

            segment = QtGui.QGraphicsLineItem(QtCore.QLineF(prevViewPos, currViewPos))
            segment.setPen(self.roiPen)

            self.imageView.addItem(segment)

            self.region.vertices.append(currItemPos)
            self.region.segments.append(segment)

        self.prevItemPos = currItemPos

    """
    Subroutine to create stepwise segments when distance between prev and curr mouse position is greater 
    than 1 pixel.
    """
    def interpolateSegments(self, currItemPos, prevItemPos = None):
        if prevItemPos == None:
            prevItemPos = self.prevItemPos

        xRange = int(abs(currItemPos.x() - prevItemPos.x())) + 1
        yRange = int(abs(currItemPos.y() - prevItemPos.y())) + 1

        stepRange = xRange if xRange > yRange else yRange

        # maybe add functionality later to have a consistent slope
        # xSlope = 1 if xRange > yRange else math.floor(yRange / xRange)
        # ySlope = 1 if yRange > xRange else math.floor(xRange / yRange)

        xSign = 1 if currItemPos.x() > prevItemPos.x() else -1
        ySign = 1 if currItemPos.y() > prevItemPos.y() else -1

        _currItemPos = prevItemPos
        _currViewPos = self.imageView.mapFromItemToView(self.imageItem, _currItemPos)

        for step in range(1, stepRange):
            if step == 1:
                _prevItemPos = prevItemPos
                _prevViewPos = self.imageView.mapFromItemToView(self.imageItem, _prevItemPos)

            if step < xRange:
                _currItemPos = QtCore.QPointF((_prevItemPos.x() + xSign), _prevItemPos.y())
                _currViewPos = self.imageView.mapFromItemToView(self.imageItem, _currItemPos)

                segment = QtGui.QGraphicsLineItem(QtCore.QLineF(_prevViewPos, _currViewPos))
                segment.setPen(self.roiPen)
                self.imageView.addItem(segment)
                self.region.vertices.append(_currItemPos)
                self.region.segments.append(segment)

            _prevItemPos = _currItemPos
            _prevViewPos = self.imageView.mapFromItemToView(self.imageItem, _prevItemPos)

            if step < yRange:
                _currItemPos = QtCore.QPointF(_currItemPos.x(), (_prevItemPos.y() + ySign))
                _currViewPos = self.imageView.mapFromItemToView(self.imageItem, _currItemPos)

                segment = QtGui.QGraphicsLineItem(QtCore.QLineF(_prevViewPos, _currViewPos))
                segment.setPen(self.roiPen)
                self.imageView.addItem(segment)
                self.region.vertices.append(_currItemPos)
                self.region.segments.append(segment)

            _prevItemPos = _currItemPos
            _prevViewPos = self.imageView.mapFromItemToView(self.imageItem, _prevItemPos)

    """
    Clears all existing overlays.
    """
    def clear(self):
        for region in self.overlay.regions:
            if len(region.segments) > 0:
                for segment in region.segments:
                    self.imageView.removeItem(segment)

        self.overlay = Overlay()

    """
    Updates the overlay to match the mask.
    ================== ===========================================================================
    **Arguments:**
    mask               mask object containing all independent masks
    ================== ===========================================================================
    """
    def newMask(self, mask):
        self.clear()

        for region in mask.regions:
            mask = region.mask
            mask = np.uint8(mask * 255).T

            # finds all independent contours from a given mask.
            contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

            # iterate over each contour and store in regions
            for contour in contours:
                points = []

                # the problem here is findcontours creates diagonals instead of following a perfect
                # vertical/horizontal path. we can try and fix that here
                prevX = None
                prevY = None
                for point in contour:
                    x = point[0][0]
                    y = point[0][1]

                    if prevX and prevY:
                        dist = math.dist([x, prevY], [prevX, y])

                        if dist > 1:
                            if (x > prevX) and (y < prevY):
                                points.append(QtCore.QPointF(prevX, y))
                            elif (x < prevX) and (y < prevY):
                                points.append(QtCore.QPointF(x, prevY))
                            elif (x < prevX) and (y > prevY):
                                points.append(QtCore.QPointF(prevX, y))
                            elif (x > prevX) and (y > prevY):
                                points.append(QtCore.QPointF(x, prevY))

                    prevX = x
                    prevY = y

                    points.append(QtCore.QPointF(x, y))

                self.region = SegmentationRegion()
                self.region.color = region.color
                self.region.id = region.id if region.id is not None else SegmentationRegion.DEFAULT
                self.region.vertices = points
                self.overlay.regions.append(self.region)

        # iterate over each region and draw segments
        for region in self.overlay.regions:
            if region.id == SegmentationRegion.BACKGROUND:
                _pen = QPen(self.bgPen)
            else:
                _pen = QPen(self.roiPen)

            if region.color is not None:
                _pen.setColor(region.color)

            vertices = region.vertices

            for index, point in enumerate(vertices):
                if index == 0:
                    segment = QtGui.QGraphicsLineItem(QtCore.QLineF(vertices[index], vertices[-1]))
                else:
                    segment = QtGui.QGraphicsLineItem(QtCore.QLineF(vertices[index], vertices[index - 1]))

                segment.setPen(_pen)
                self.imageView.addItem(segment)
                region.segments.append(segment)

    def checkROICollision(self, ev):
        if not self.enabled:
            return

        try:
            currItemPos = ev.pos()

        except:
            return

        # clamp item position to image vertices
        currItemPos = QtCore.QPointF(round(currItemPos.x()), round(currItemPos.y()))
        currItemPos = [currItemPos.x(), currItemPos.y()]

        for region in self.overlay.regions:
            vertices = [[vertice.x(), vertice.y()] for vertice in region.vertices]

            distances = [math.dist(currItemPos, vertice) for vertice in vertices]

            if np.min(distances) < 2:
                self.showContextMenu(ev, region)

                return

    def showContextMenu(self, ev, region):
        viewPos = self.imageView.mapFromItemToView(self.imageItem, ev.pos())
        scenePos = self.imageView.mapViewToScene(viewPos)
        globalPos = self.imageView.getViewWidget().mapToGlobal(scenePos.toPoint())

        menu = QMenu()

        setROI = None
        setBG = None
        setID = None

        if region.id == SegmentationRegion.BACKGROUND:
            setROI = menu.addAction("Set ROI")
        else:
            setBG = menu.addAction("Set Background")
            setID = menu.addAction("Rename ROI" + " (Current: " + region.id + ")")

        action = menu.exec_(globalPos)

        if action is None:
            return

        if action == setBG:
            region.id = SegmentationRegion.BACKGROUND

            for segment in region.segments:
                _pen = QPen(self.bgPen)
                _pen.setColor(segment.pen().color())
                segment.setPen(_pen)

            self.newOverlay.emit(self.overlay)

        elif action == setROI:
            region.id = SegmentationRegion.DEFAULT

            for segment in region.segments:
                _pen = QPen(self.roiPen)
                _pen.setColor(segment.pen().color())
                segment.setPen(_pen)

            self.newOverlay.emit(self.overlay)

        elif action == setID:
            idDialog = InputDialog()
            inputText, okPressed = idDialog.getText(idDialog, "ROI", "Set ROI Name:", QLineEdit.Normal, "")

            if not okPressed:
                return

            if not inputText:
                return

            if inputText == SegmentationRegion.BACKGROUND:
                inputText = SegmentationRegion.BACKGROUND + '(1)'

            elif inputText == SegmentationRegion.DEFAULT:
                inputText = SegmentationRegion.DEFAULT + '(1)'

            region.id = inputText

            self.newOverlay.emit(self.overlay)


class Overlay:
    def __init__(self):
        self.regions = []


class InputDialog(QInputDialog):
    def __init__(self):
        super().__init__()

