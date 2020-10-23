from PyQt5.QtWidgets import QTableWidget, QAbstractScrollArea, QTableWidgetItem, QHBoxLayout, QWidget, QCheckBox
from PyQt5.QtWidgets import QFrame, QAbstractItemView
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from scripts.DICOM.Sequence import Sequence


"""
Widget used to display patient data in table format.
"""
class PatientTableView(QTableWidget):
    seriesSelected = pyqtSignal(object)
    sequenceSelected = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setFrameShape(QFrame.NoFrame)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)

        self.setShowGrid(True)
        self.setGridStyle(Qt.SolidLine)

        self.verticalHeader().setVisible(False)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.headers = ['Active', 'Patient ID', 'Study ID', 'Sequence',
                        'Series #', '# Images', 'Venc', 'Image Type', 'BPM']

        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.adjustColumnWidths(initial=True)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)
        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet()

    """
    Called when new patient is loaded. Calls reset and display series functions
    ================== ===========================================================================
    **Arguments:**
    patient            loaded patient
    ================== ===========================================================================
    """
    def newPatient(self, patient):
        self.clear()

        self.displayAvailableSeries(patient)

    """
    Resets and clears table
    """
    def clear(self):
        super().clear()
        self.setRowCount(0)

    """
    Loads each series for a given patient and displays it's relevant information
    ================== ===========================================================================
    **Arguments:**
    patient            loaded patient
    ================== ===========================================================================
    """
    def displayAvailableSeries(self, patient):
        self.headers = ['Active', 'Patient ID', 'Study ID', 'Sequence',
                        'Series #', '# Images', 'Venc', 'Image Type', 'BPM']
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)

        patientId = patient.getPatientID()

        for study in patient.studies:
            studyId = study.getStudyID()

            for series in study.series:
                sequence = Sequence(refSeries=series, study=study)
                series.parentSequence = sequence

                sequenceName = str(series.parentSequence.name)
                seriesNumber = str(series.getSeriesNumber())
                numImages = str(len(series.images))
                bpm = str(series.getBPM())
                venc = str(series.getVenc())
                seriesType = str(series.getReconstructionType())

                rowPosition = self.rowCount()
                self.insertRow(rowPosition)

                seriesToggle = Toggle(series)
                seriesToggle.toggled.connect(self.seriesToggled)

                self.setCellWidget(rowPosition, 0, seriesToggle)
                self.setItem(rowPosition, 1, CellItem(patientId))
                self.setItem(rowPosition, 2, CellItem(studyId))
                self.setItem(rowPosition, 3, CellItem(sequenceName))
                self.setItem(rowPosition, 4, CellItem(seriesNumber))
                self.setItem(rowPosition, 5, CellItem(numImages))
                self.setItem(rowPosition, 6, CellItem(venc))
                self.setItem(rowPosition, 7, CellItem(seriesType))
                self.setItem(rowPosition, 8, CellItem(bpm))

        delegate = AlignDelegate(self)
        self.setItemDelegate(delegate)
        self.adjustColumnWidths()

    """
    Called when a series is selected. Emits a signal containing active series
    ================== ===========================================================================
    **Arguments:**
    activeToggle       the toggle associated with the selected series
    ================== ===========================================================================
    """
    def seriesToggled(self, activeToggle):
        if activeToggle.chkBox.isChecked():
            self.seriesSelected.emit(activeToggle.series)

        else:
            self.seriesSelected.emit(None)

        # uncheck any other active series toggles
        for row in range(0, self.rowCount()):
            toggle = self.cellWidget(row, 0)

            if toggle != activeToggle:
                toggle.chkBox.setChecked(False)

    """
    Called when view area of table is resized. Calls adjust column widths function
    ================== ===========================================================================
    **Arguments:**
    event              pyqt event associated with resize event
    ================== ===========================================================================
    """
    def resizeEvent(self, event):
        self.adjustColumnWidths()

    """
    Adjusts column widths to fit data. If initial is set to True, adjusts column sizes with no data
    ================== ===========================================================================
    **Arguments:**
    initial            column width adjustment is slightly different based on if table has data
    ================== ===========================================================================
    """
    def adjustColumnWidths(self, initial=None):
        self.resizeColumnToContents(0)

        if initial is not None:
            startingIndex = 0
            offset = 0

        else:
            startingIndex = 1
            offset = 65

        proposedColWidth = (self.frameGeometry().width() -
                            self.columnWidth(0) - offset) / (self.columnCount() - startingIndex)

        for column in range(startingIndex, self.columnCount()):
            minColWidth = self.sizeHintForColumn(column)

            if (proposedColWidth > minColWidth):
                self.setColumnWidth(column, proposedColWidth)

            else:
                self.setColumnWidth(column, minColWidth)

        self.horizontalHeader().setStretchLastSection(True)

    """
    Sets stylesheet for table view
    """
    def setStyleSheet(self):
        super().setStyleSheet("QTableWidget{border: 1px solid gray;}"
                              "QTableWidget::item{"
                              "border-color: rgb(44, 49, 60);"
                              "padding-left: 5px;"
                              "padding-right: 5px;"
                              "gridline-color: rgb(44, 49, 60);"
                              "}"
                              "QTableWidget::item:selected{"
                              "background-color: rgb(85, 170, 255);"
                              "}"
                              "QHeaderView::section{"
                              "background-color: rgb(39, 44, 54);"
                              "max-width: 30px;"
                              "border: 1px solid rgb(44, 49, 60);"
                              "border-style: none;"
                              "border-bottom: 1px solid rgb(44, 49, 60);"
                              "border-right: 1px solid rgb(44, 49, 60);"
                              "}"
                              ""
                              "QTableWidget::horizontalHeader {"
                              "background-color: rgb(81, 255, 0);"
                              "}"
                              "QHeaderView::section:horizontal"
                              "{"
                              "border: 1px solid rgb(32, 34, 42);"
                              "background-color: rgb(27, 29, 35);"
                              "padding: 3px;"
                              "}"
                              "QHeaderView::section:vertical"
                              "{"
                              "border: 1px solid rgb(44, 49, 60);"
                              "}"
                              "")

"""
Widget containing a center-aligned checkbox.
"""
class Toggle(QWidget):
    toggled = pyqtSignal(object)

    def __init__(self, series):
        super().__init__()

        self.series = series

        self.initUI()

        self.chkBox.clicked.connect(self.clicked)

    def initUI(self):
        self.centralFrame = QFrame(self)

        self.chkBox = QCheckBox(self.centralFrame)
        self.chkBox.setContentsMargins(0, 0, 0, 0)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.setAlignment(Qt.AlignCenter)
        self.centralLayout.addWidget(self.chkBox)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)
        self.setContentsMargins(0, 0, 0, 0)

        self.centralFrame.setStyleSheet(u"background-color: rgb(15, 15, 15);")

    def clicked(self):
        self.toggled.emit(self)


class CellItem(QTableWidgetItem):
    def __init__(self, item):
        super().__init__(item)
        self.setFlags(Qt.NoItemFlags)


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
