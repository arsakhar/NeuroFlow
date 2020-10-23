import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QFrame, QHBoxLayout
from PyQt5.QtGui import QColor, QPen
from PyQt5 import Qt

from scripts.ToolBox.FlowToolbox import FlowToolbox


"""
Plots flow curve
"""
class FlowGraphicsView(pg.PlotWidget):
    def __init__(self, parent, toolBar):
        self.plotItem = PlotItem()
        super().__init__(parent, plotItem=self.plotItem)

        self.toolBar = toolBar
        self.toolBar.clearBtn.clicked.connect(self.clear)

        self.plotDataItems = []

        self.legendItem = LegendItem(self.plotItem)

        self.toolTip = TextItem()

        self.series = None
        self.sequence = None

        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.plotItem.showGrid(True, True)
        self.plotItem.setMenuEnabled(False)

        self.toolTip.setText('')
        self.toolTip.setColor((255, 255, 0))
        self.toolTip.setAnchor((1, 1))
        self.toolTip.show()

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.centralFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)

        self.show()

    """
    Called when new patient is loaded. Calls clear function
    ================== ===========================================================================
    **Arguments:**
    patient            loaded patient
    ================== ===========================================================================
    """
    def newPatient(self, patient):
        self.series = None
        self.sequence = None

        self.clearPlot()

    """
    Resets and clears plot
    """
    def clearPlot(self):
        try:
            self.plotItem.scene().sigMouseMoved.disconnect(self.onMouseMove)
        except:
            pass

        self.plotDataItems.clear()
        self.legendItem.clear()
        self.plotItem.clear()

    """
    Called when a new imageROI is created. Calls plot method
    ================== ===========================================================================
    **Arguments:**
    segmentationBundle segmentations
    ================== ===========================================================================
    """
    def newSegmentationBundle(self, segmentationBundle):
        if self.series is None:
            return

        flowToolbox = FlowToolbox()
        phaseSeries = self.series.parentSequence.getSeriesByType("Phase")

        if phaseSeries is None:
            return

        regions = segmentationBundle.regions

        if not regions:
            return

        for region in regions:
            # Need to convert the image ROIData to phase ROIData. This is necessary because flow can only be
            # calculated off the phase image, not the magnitude or complex difference image.
            region.image = flowToolbox.imageROItoPhaseROI(imageROI=region.image, imageSeries=self.series,
                                                      phaseSeries=phaseSeries)

        self.series = phaseSeries

        self.plot(regions)

    """
    Called when a mouse moves over plot area. if mouse hovers over plot point, shows it in tooltip
    ================== ===========================================================================
    **Arguments:**
    pos                mouse scene position
    ================== ===========================================================================
    """
    def onMouseMove(self, pos):
        for dataItem in self.plotItem.dataItems:
            mousePos = dataItem.mapFromScene(pos)
            pointsAtPos = dataItem.scatter.pointsAt(mousePos)

            if len(pointsAtPos) == 1:
                pointsAtPos = pointsAtPos[0]

                time = int(pointsAtPos.pos().x())
                flowRate = int(pointsAtPos.pos().y())

                self.toolTip.setText('(' + str(time) + ', ' + str(flowRate) + ')')
                self.toolTip.setPos(mousePos.x(), mousePos.y())
                self.toolTip.show()

                break

            else:
                self.toolTip.hide()

    """
    Displays a plot of flow data
    ================== ===========================================================================
    **Arguments:**
    ROI                ROI ndarray
    ================== ===========================================================================
    """
    def plot(self, regions):
        flowToolbox = FlowToolbox()

        self.clearPlot()

        self.plotItem.scene().sigMouseMoved.connect(self.onMouseMove)

        for index, region in enumerate(regions):
            plotDataItem = PlotDataItem(self)

            color = QColor(PlotDataItem.colors[index % len(PlotDataItem.colors)])

            plotDataItem.linePen.setColor(color)
            plotDataItem.symbolPen.setColor(color)

            ROI = region.image

            area = flowToolbox.getArea(ROI, self.series.images[0].getPixelArea())
            timeData = flowToolbox.getTimeData(self.series.getRRInterval(), len(self.series.images))
            velocityData = flowToolbox.getVelocityData(ROI, self.series.getVenc())
            flowData = flowToolbox.getFlowData(velocityData, area)

            plotDataItem.setData(np.array(timeData), np.array(flowData))
            self.plotItem.addItem(plotDataItem)

            self.legendItem.addItem(plotDataItem, region.id)

            self.plotDataItems.append(plotDataItem)

        self.plotItem.addItem(self.toolTip)

    """
    Called when a new series is selected
    ================== ===========================================================================
    **Arguments:**
    series             the series object
    ================== ===========================================================================
    """
    def seriesSelected(self, series):
        self.clearPlot()

        self.series = series

        if self.series is not None:
            self.sequence = series.parentSequence

    """
    Override mouse wheel event and ignore ev input
    """
    def wheelEvent(self, ev, axis=None):
        ev.ignore()


"""
A plot item for displaying flow curves
"""
class PlotItem(pg.PlotItem):
    def __init__(self, image=None):
        super().__init__(image=image)

        self.setTitle("Flow Curve")
        self.setLabel(axis='bottom', text='Time (ms)')
        self.setLabel(axis='left', text='Flow Rate (mm3/s)')


"""
A text item for displaying plot points on mouse hover
"""
class TextItem(pg.TextItem):
    def __init__(self):
        super().__init__()


"""
A legend item for displaying legend
"""
class LegendItem(pg.LegendItem):
    def __init__(self, plotItem):
        super().__init__()

        self.setParentItem(plotItem)

        self.setOffset((500, 5))


"""
A legend item for displaying legend
"""
class PlotDataItem(pg.PlotDataItem):
    colors = ['red', 'cyan', 'green', 'blue', 'yellow', 'orange', 'pink', 'violet', 'indigo', 'chocolate']

    def __init__(self, parent):
        self.linePen = QPen()
        self.linePen.setWidthF(.1)

        self.symbolPen = QPen()
        self.symbolPen.setWidthF(.1)

        super().__init__(connect='all', symbol='o', pen=self.linePen, symbolPen=self.symbolPen)

        self.setSymbolSize(5)
