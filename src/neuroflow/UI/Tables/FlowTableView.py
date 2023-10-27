from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractScrollArea, QTableWidgetItem, QFrame, QAbstractItemView
from PyQt5.QtWidgets import QCheckBox, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

from ...ToolBox.FlowPresets import FlowPresets
from ...ToolBox.FlowToolbox import FlowToolbox


"""
Widget to output results of flow analysis
"""
class FlowTableView(QWidget):
    newData = pyqtSignal(object)

    def __init__(self, parent, toolBar):
        super().__init__(parent)

        self.toolBar = toolBar

        self.series = None
        self.regions = None

        self.initUI()

        self.presetsPanel.presetSelected.connect(self.presetSelected)
        self.toolBar.clearBtn.clicked.connect(self.tableView.clear)

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.uiFrame = QFrame(self.centralFrame)
        self.uiFrame.setFrameShape(QFrame.NoFrame)
        self.uiFrame.setFrameShadow(QFrame.Raised)
        self.uiFrame.setContentsMargins(0, 0, 0, 0)
        self.uiFrame.setStyleSheet("border: none;")

        self.tableView = TableView(self.uiFrame)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.presetsPanel = PresetsPanel(self.uiFrame)

        self.uiLayout = QVBoxLayout(self.uiFrame)
        self.uiLayout.addWidget(self.presetsPanel)
        self.uiLayout.addWidget(self.tableView)
        self.uiLayout.setContentsMargins(0, 0, 0, 0)

        self.centralLayout = QVBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.uiFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)

    """
    Called when new patient is loaded. Resets existing table
    ================== ===========================================================================
    **Arguments:**
    patient            loaded patient
    ================== ===========================================================================
    """
    def newPatient(self, patient):
        self.clear()

    """
    Resets and clears table
    """
    def clear(self):
        self.series = None
        self.regions = None
        self.tableView.clear()

    """
    Runs analysis if selected preset is active and the ROI and series are not none
    ================== ===========================================================================
    **Arguments:**
    activePreset       the preset option selected in the panel
    ================== ===========================================================================
    """
    def presetSelected(self, activePreset):
        if (activePreset is None) or (self.regions is None) or (self.series is None):
            self.tableView.clear()

            return

        self.runAnalysis()

    """
    Called when a new set of segmentations are created. Calls run analysis method if an active preset exists
    ================== ===========================================================================
    **Arguments:**
    segmentationBundle segmentations
    ================== ===========================================================================
    """
    def newSegmentationBundle(self, segmentationBundle):
        if self.presetsPanel.activePreset is None:
            return

        regions = segmentationBundle.regions

        if not regions:
            return

        flowToolbox = FlowToolbox()
        phaseSeries = self.series.parentSequence.getSeriesByType("Phase")

        # did we load the series containing the phase images?
        if phaseSeries is None:
            return

        for region in regions:
            # Need to convert the image ROIData to phase ROIData. This is necessary because flow can only be
            # calculated off the phase image, not the magnitude or complex difference image.
            region.image = flowToolbox.imageROItoPhaseROI(imageROI=region.image, imageSeries=self.series,
                                                      phaseSeries=phaseSeries)


        self.series = phaseSeries
        self.regions = regions

        self.runAnalysis()

    """
    Runs the analysis. Calls a specific analysis based on active preset
    """
    def runAnalysis(self):
        activePreset = self.presetsPanel.activePreset

        flowPresets = FlowPresets(activePreset.lower())

        for region in self.regions:
            if activePreset == FlowPresets.AQUEDUCT:
                singleMeasures, pairedMeasures = flowPresets.getAqueductMeasures(region.image, self.series)

            elif activePreset == FlowPresets.C2_C3_SS:
                singleMeasures, pairedMeasures = flowPresets.getC2C3Measures(region.image, self.series)

            elif activePreset == FlowPresets.ARTERY:
                singleMeasures, pairedMeasures = flowPresets.getArteryMeasures(region.image, self.series)

            elif activePreset == FlowPresets.VEIN:
                singleMeasures, pairedMeasures = flowPresets.getVeinMeasures(region.image, self.series)

            else:
                singleMeasures, pairedMeasures = flowPresets.getDefaultMeasures(region.image, self.series)

            region.measures = [singleMeasures, pairedMeasures]

        self.tableView.update(self.regions)

    """
    Called when a new series is selected
    ================== ===========================================================================
    **Arguments:**
    series             the series object
    ================== ===========================================================================
    """
    def seriesSelected(self, series):
        self.clear()

        if series is None:
            return

        self.series = series

    """
    Called when view area of table is resized. Calls adjust presets and column widths function
    ================== ===========================================================================
    **Arguments:**
    event              pyqt event associated with resize event
    ================== ===========================================================================
    """
    def resizeEvent(self, event):
        self.presetsPanel.adjustSpacing()
        self.tableView.adjustColumnWidths()


"""
Widget containing analysisWidget preset checkboxes
"""
class PresetsPanel(QWidget):
    presetSelected = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.label = QLabel(self)

        self.presets = ['Default', 'Aqueduct', 'C2-C3 SS', 'Artery', 'Vein']

        self.presetChkBoxes = []
        self.activePreset = None

        self.layout = QGridLayout()

        self.initUI()

    def initUI(self):
        self.label.setText("Presets: ")
        font = QFont()
        font.setBold(True)

        self.label.setFont(font)

        self.layout.addWidget(self.label, 0, 0)

        for index, preset in enumerate(self.presets):
            presetChkBox = CheckBox(self, preset)
            if preset == 'Default':
                presetChkBox.setChecked(True)
                self.activePreset = preset

            presetChkBox.toggled.connect(self.presetToggled)
            self.presetChkBoxes.append(presetChkBox)
            self.layout.addWidget(presetChkBox, 0, index + 1)

        self.layout.setAlignment(Qt.AlignLeft)
        self.setLayout(self.layout)

        self.adjustSpacing()
        self.show()
        self.setContentsMargins(0, 0, 0, 0)

    def adjustSpacing(self):
        self.layout.setHorizontalSpacing(25)

    def presetToggled(self, activePresetChkBox):
        for presetChkBox in self.presetChkBoxes:
            if activePresetChkBox == presetChkBox:
                continue

            presetChkBox.setChecked(False)

        if activePresetChkBox.isChecked():
            self.activePreset = activePresetChkBox.preset
            self.presetSelected.emit(self.activePreset)
        else:
            self.activePreset = None
            self.presetSelected.emit(None)


"""
Widget for creating preset checkboxes
"""
class CheckBox(QCheckBox):
    toggled = pyqtSignal(object)

    def __init__(self, parent, preset):
        super().__init__(parent)
        self.preset = preset

        self.clicked.connect(self.stateToggled)

        self.initUI()

    def initUI(self):
        self.setText(self.preset)
        self.setContentsMargins(0, 0, 0, 0)

    def stateToggled(self):
        self.toggled.emit(self)


"""
Widget containing a table for displaying analysisWidget results
"""
class TableView(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.initUI()

    def initUI(self):
        self.setRowCount(35)
        self.setColumnCount(5)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.adjustColumnWidths()
        self.setContentsMargins(0, 0, 0, 0)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)

    def clear(self):
        super().clear()

        self.setRowCount(35)
        self.setColumnCount(5)

    """
    Updates the table view for the analysis widget
    ================== ===========================================================================
    **Arguments:**
    regions            segmentation regions containing analysis measurements
    ================== ===========================================================================
    """
    def update(self, regions):
        super().update()

        self.setColumnCount(10)
        self.setRowCount(0)

        colPosition = 0

        for region in regions:
            rowPosition = 0

            if colPosition >= self.columnCount():
                self.insertColumn(colPosition)
                self.insertColumn(colPosition + 1)

            if rowPosition > (self.rowCount() - 1):
                self.insertRow(rowPosition)

            self.setItem(rowPosition, colPosition, CellItem(str('ID')))
            self.setItem(rowPosition, colPosition + 1, CellItem(str(region.id)))

            rowPosition += 1

            for key, value in region.measures[0].items():
                if key == 'Preset':
                    continue

                if rowPosition > (self.rowCount() - 1):
                    self.insertRow(rowPosition)

                self.setItem(rowPosition, colPosition, CellItem(str(key)))
                self.setItem(rowPosition, colPosition + 1, CellItem(str(value)))

                rowPosition += 1

            if rowPosition > (self.rowCount() - 1):
                self.insertRow(rowPosition)

            rowPosition += 1

            for (key, value) in region.measures[1].items():
                if rowPosition > (self.rowCount() - 1):
                    self.insertRow(rowPosition)

                keyOne, keyTwo = key.split(':')
                keyOne = keyOne.strip()
                keyTwo = keyTwo.strip()

                valuesOne, valuesTwo = value

                self.setItem(rowPosition, colPosition, CellItem(str(keyOne)))
                self.setItem(rowPosition, colPosition + 1, CellItem(str(keyTwo)))

                rowPosition += 1

                for valOne, valTwo in zip(valuesOne, valuesTwo):
                    if rowPosition > (self.rowCount() - 1):
                        self.insertRow(rowPosition)

                    self.setItem(rowPosition, colPosition, CellItem(str(valOne)))
                    self.setItem(rowPosition, colPosition + 1, CellItem(str(valTwo)))

                    rowPosition += 1

                rowPosition += 1

            colPosition += 3

        self.adjustColumnWidths()
        delegate = AlignDelegate(self)
        self.setItemDelegate(delegate)

    def adjustColumnWidths(self):
        proposedColWidth = ((self.parent.frameGeometry().width() - 35) / self.columnCount())

        for column in range(0, self.columnCount()):
            minColWidth = self.sizeHintForColumn(column)

            if (proposedColWidth > minColWidth):
                self.setColumnWidth(column, proposedColWidth)

            else:
                self.setColumnWidth(column, minColWidth)

        self.horizontalHeader().setStretchLastSection(True)


class CellItem(QTableWidgetItem):
    def __init__(self, item):
        super().__init__(item)
        self.setFlags(Qt.NoItemFlags)


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
