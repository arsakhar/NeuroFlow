import math

import cv2
import numpy as np
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QGraphicsObject, QMenu, QInputDialog, QLineEdit, QGraphicsLineItem
from shapely.geometry import Polygon

from ...Helper.SegmentationRegion import SegmentationRegion


class OverlayGraphics(QGraphicsObject):
    """
    QGraphicsObject for managing overlay drawing on an image.

    Parameters
    ----------
    imageView : QGraphicsView
        The view where the image is displayed.

    imageItem : QGraphicsPixmapItem
        The image item to overlay on.

    toolBar : ToolBar
        The toolbar object for overlay control.

    settings : Settings
        The settings object.

    """

    newOverlay = pyqtSignal(object)
    updatedOverlay = pyqtSignal(object)

    def __init__(self, imageView, imageItem, toolBar, settings):
        """
        Initializes the OverlayGraphics object.

        Parameters
        ----------
        imageView : QGraphicsView
            The view where the image is displayed.

        imageItem : QGraphicsPixmapItem
            The image item to overlay on.

        toolBar : ToolBar
            The toolbar object for overlay control.

        settings : Settings
            The settings object.

        """

        super().__init__()
        self.imageView = imageView
        self.imageItem = imageItem

        self.toolBar = toolBar

        self.settings = settings

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
        """
        Resets the overlay state by unsubscribing from mouse events and clearing existing overlays.

        """

        self.unsubscribe()
        self.clear()
        self.enabled = False

    def newPatient(self, patient):
        """
        Resets the overlay when a new patient is loaded.

        Parameters
        ----------
        patient : Patient
            The new patient object.

        """

        self.reset()

    def setOverlay(self, overlayColor):
        """
        Sets the color of the overlay pen.

        Parameters
        ----------
        overlayColor : str
            Hex color code.

        """

        if overlayColor is None:
            self.enabled = False
            return

        self.enabled = True

        color = QColor(overlayColor)
        self.roiPen.setColor(color)

    def seriesSelected(self, series):
        """
        Handles series selection event.

        Parameters
        ----------
        series : Series
            The selected series object.

        """

        self.reset()

        if series is None:
            return

        elif series.parentSequence.getSeriesByType("Phase") is None:
            return

        self.subscribe()

    def subscribe(self):
        """
        Enables overlay drawing by subscribing to mouse events.

        """

        self.imageItem.leftMouseDragged.connect(self.drawOnMouseDrag)
        self.imageItem.contextMenuTriggered.connect(self.checkROICollision)

    def unsubscribe(self):
        """
        Disables overlay drawing by unsubscribing from mouse events.

        """

        self.toolBar.overlayBtn.activeSeg = None

        try:
            self.imageItem.leftMouseDragged.disconnect(self.drawOnMouseDrag)

        except:
            pass

        try:
            self.imageItem.contextMenuTriggered.disconnect(self.checkROICollision)

        except:
            pass

    def drawOnMouseDrag(self, ev):
        """
        Draws the overlay while the mouse is being dragged.

        Parameters
        ----------
        ev : QMouseEvent
            Mouse event object.

        """

        if not self.enabled:
            return

        currItemPos = ev.pos()

        # Clamp item position to image vertices
        currItemPos = QtCore.QPointF(round(currItemPos.x()), round(currItemPos.y()))

        if ev.isStart():
            self.region = SegmentationRegion()
            self.region.polygon = Polygon()
            self.region.id = SegmentationRegion.DEFAULT
            self.region.color = self.roiPen.color()

            self.region.vertices.append(currItemPos)
            self.region.prevItemPos = currItemPos

            return

        if ev.isFinish():
            initialItemPos = self.region.vertices[0]

            self.drawSegment(startItemPos=initialItemPos, endItemPos=currItemPos)

            self.overlay.regions.append(self.region)

            # Emit overlay
            self.newOverlay.emit(self.overlay)

            return

        # Do not add redundant vertices
        if (currItemPos == self.region.prevItemPos) | (currItemPos in self.region.vertices):
            return

        self.drawSegment(startItemPos=self.region.prevItemPos, endItemPos=currItemPos)

        self.region.prevItemPos = currItemPos

    def drawSegment(self, startItemPos, endItemPos):
        """
        Draw a segmented line between two points and update the region.

        Parameters
        ----------
        startItemPos : QPointF
            Starting mouse position.

        endItemPos : QPointF
            Ending mouse position.

        """

        num_x_segments = int(abs(endItemPos.x() - startItemPos.x()))
        num_y_segments = int(abs(endItemPos.y() - startItemPos.y()))

        num_segments = num_x_segments if num_x_segments > num_y_segments else num_y_segments

        x_segment_direction = 1 if endItemPos.x() > startItemPos.x() else -1
        y_segment_direction = 1 if endItemPos.y() > startItemPos.y() else -1

        currItemPos = startItemPos

        prevItemPos = startItemPos
        prevViewPos = self.imageView.mapFromItemToView(self.imageItem, prevItemPos)

        for segment_num in range(1, num_segments + 1):
            if segment_num <= num_x_segments:
                currItemPos = QtCore.QPointF((prevItemPos.x() + x_segment_direction), prevItemPos.y())
                currViewPos = self.imageView.mapFromItemToView(self.imageItem, currItemPos)

                segment = QGraphicsLineItem(QtCore.QLineF(prevViewPos, currViewPos))
                segment.setPen(self.roiPen)
                self.imageView.addItem(segment)
                self.region.vertices.append(currItemPos)
                self.region.segments.append(segment)

            prevItemPos = currItemPos
            prevViewPos = self.imageView.mapFromItemToView(self.imageItem, prevItemPos)

            if segment_num <= num_y_segments:
                currItemPos = QtCore.QPointF(currItemPos.x(), (prevItemPos.y() + y_segment_direction))
                currViewPos = self.imageView.mapFromItemToView(self.imageItem, currItemPos)

                segment = QGraphicsLineItem(QtCore.QLineF(prevViewPos, currViewPos))
                segment.setPen(self.roiPen)
                self.imageView.addItem(segment)
                self.region.vertices.append(currItemPos)
                self.region.segments.append(segment)

            prevItemPos = currItemPos
            prevViewPos = self.imageView.mapFromItemToView(self.imageItem, prevItemPos)

    def clear(self):
        """
        Clears all existing overlays.

        """

        for region in self.overlay.regions:
            if len(region.segments) > 0:
                for segment in region.segments:
                    self.imageView.removeItem(segment)

        self.overlay = Overlay()

    def newMask(self, mask):
        """
        Updates the overlay to match the mask.

        Parameters
        ----------
        mask : Mask
            Mask object containing all independent masks.

        """

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
                    segment = QGraphicsLineItem(QtCore.QLineF(vertices[index], vertices[-1]))
                else:
                    segment = QGraphicsLineItem(QtCore.QLineF(vertices[index], vertices[index - 1]))

                segment.setPen(_pen)
                self.imageView.addItem(segment)
                region.segments.append(segment)

    def checkROICollision(self, ev):
        """
        Checks for collision with existing ROIs.

        Parameters
        ----------
        ev : QMouseEvent
            Mouse event object.

        """

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
        """
        Displays a context menu for selecting ROI options.

        Parameters
        ----------
        ev : QMouseEvent
            Mouse event object.

        region : SegmentationRegion
            The selected region.

        """

        viewPos = self.imageView.mapFromItemToView(self.imageItem, ev.pos())
        scenePos = self.imageView.mapViewToScene(viewPos)
        globalPos = self.imageView.getViewWidget().mapToGlobal(scenePos.toPoint())

        menu = QMenu()

        # setROI = None
        # setBG = None
        # setID = None

        for label in self.settings.labels:
            menu.addAction(label)

        # if region.id == SegmentationRegion.BACKGROUND:
        #     setROI = menu.addAction("Set ROI")
        # else:
        #     setBG = menu.addAction("Set Background")
        #     setID = menu.addAction("Rename ROI" + " (Current: " + region.id + ")")

        action = menu.exec_(globalPos)

        if action is None:
            return

        # if action == setBG:
        #     region.id = SegmentationRegion.BACKGROUND
        #
        #     for segment in region.segments:
        #         _pen = QPen(self.bgPen)
        #         _pen.setColor(segment.pen().color())
        #         segment.setPen(_pen)
        #
        #     self.newOverlay.emit(self.overlay)
        #
        # elif action == setROI:
        #     region.id = SegmentationRegion.DEFAULT
        #
        #     for segment in region.segments:
        #         _pen = QPen(self.roiPen)
        #         _pen.setColor(segment.pen().color())
        #         segment.setPen(_pen)
        #
        #     self.newOverlay.emit(self.overlay)
        #
        # elif action == setID:
        #     idDialog = InputDialog()
        #     inputText, okPressed = idDialog.getText(idDialog, "ROI", "Set ROI Name:", QLineEdit.Normal, "")
        #
        #     if not okPressed:
        #         return
        #
        #     if not inputText:
        #         return
        #
        #     if inputText == SegmentationRegion.BACKGROUND:
        #         inputText = SegmentationRegion.BACKGROUND + '(1)'
        #
        #     elif inputText == SegmentationRegion.DEFAULT:
        #         inputText = SegmentationRegion.DEFAULT + '(1)'
        #
        #     region.id = inputText

        region.id = action.text()
        self.newOverlay.emit(self.overlay)


class Overlay:
    """
    Represents an overlay containing multiple regions.

    Attributes
    ----------
    regions : list
        A list to store SegmentationRegion objects representing different regions in the overlay.

    """

    def __init__(self):
        """
        Initializes an empty overlay with no regions.

        """

        self.regions = []


class InputDialog(QInputDialog):
    """
    Custom input dialog for user interactions.

    This class extends the QInputDialog class to provide a customized input dialog
    for receiving user input.

    Attributes
    ----------
    Inherits attributes from QInputDialog.

    """

    def __init__(self):
        """
        Initializes the InputDialog object.

        This constructor initializes the custom input dialog object, inheriting
        attributes and methods from the QInputDialog class.

        """
        super().__init__()

