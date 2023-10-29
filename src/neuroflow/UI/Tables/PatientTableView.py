from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QFrame, QAbstractItemView
from PyQt5.QtWidgets import QTableWidget, QAbstractScrollArea, QTableWidgetItem, QHBoxLayout, QWidget, QCheckBox

from ...DICOM.Patient import Patient
from ...DICOM.Sequence import Sequence


class PatientTableView(QTableWidget):
    """
    A table view widget for displaying patient data.

    Parameters
    ----------
    parent : QWidget
        The parent widget.
    """

    seriesSelected = pyqtSignal(object)
    sequenceSelected = pyqtSignal(object)

    def __init__(self, parent):
        """
        Initialize the PatientTableView.

        Parameters
        ----------
        parent : QWidget
            The parent widget.

        """

        super().__init__()

        self.initUI()

    def initUI(self):
        """
        Initialize the user interface of the table view.

        """

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

    def newPatient(self, patient: Patient):
        """
        Called when a new patient is loaded. Resets and displays series for the given patient.

        Parameters
        ----------
        patient : Patient
            Loaded patient object.

        """

        self.clear()

        self.displayAvailableSeries(patient)

    def clear(self):
        """
        Resets and clears the table.

        """

        super().clear()
        self.setRowCount(0)

    def displayAvailableSeries(self, patient):
        """
        Loads each series for a given patient and displays its relevant information.

        Parameters
        ----------
        patient : Patient
            Loaded patient object.

        """

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

    def seriesToggled(self, activeToggle):
        """
        Called when a series is selected. Emits a signal containing the active series.

        Parameters
        ----------
        activeToggle : Toggle
            The toggle associated with the selected series.

        """

        if activeToggle.chkBox.isChecked():
            self.seriesSelected.emit(activeToggle.series)

        else:
            self.seriesSelected.emit(None)

        # uncheck any other active series toggles
        for row in range(0, self.rowCount()):
            toggle = self.cellWidget(row, 0)

            if toggle != activeToggle:
                toggle.chkBox.setChecked(False)

    def resizeEvent(self, event):
        """
        Called when the view area of the table is resized. Adjusts column widths accordingly.

        Parameters
        ----------
        event : QResizeEvent
            PyQt event associated with the resize event.

        """

        self.adjustColumnWidths()

    def adjustColumnWidths(self, initial=None):
        """
        Adjusts column widths to fit data. If initial is set to True, adjusts column sizes with no data.

        Parameters
        ----------
        initial : bool, optional
            Indicates whether the adjustment is initial or not.

        """

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
                self.setColumnWidth(column, int(proposedColWidth))

            else:
                self.setColumnWidth(column, minColWidth)

        self.horizontalHeader().setStretchLastSection(True)

    def setStyleSheet(self):
        """
        Sets the stylesheet for the table view.

        """

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


class Toggle(QWidget):
    """
    Widget containing a center-aligned checkbox.

    This class represents a widget containing a center-aligned checkbox, associated with a specific series object.

    Attributes
    ----------
    toggled : pyqtSignal
       Signal emitted when the checkbox is toggled.

    Methods
    -------
    __init__(self, series)
       Initialize the Toggle widget with the provided series object.

    initUI(self)
       Initialize the user interface of the Toggle widget.

    clicked(self)
       Called when the checkbox is clicked. Emits a signal indicating the toggle state.

    Notes
    -----
    Inherits from QWidget.

    Parameters
    ----------
    series : object
       Series object associated with the toggle.

    Examples
    --------
    toggle = Toggle(series_object)
    toggle.toggled.connect(toggle_handler_function)

    """

    toggled = pyqtSignal(object)

    def __init__(self, series):
        """
        Initialize the Toggle widget.

        Parameters
        ----------
        series : object
            Series object associated with the toggle.

        """

        super().__init__()

        self.series = series

        self.initUI()

        self.chkBox.clicked.connect(self.clicked)

    def initUI(self):
        """
        Initialize the user interface of the Toggle widget.

        """

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
        """
        Called when the checkbox is clicked. Emits a signal indicating the toggle state.

        """

        self.toggled.emit(self)


class CellItem(QTableWidgetItem):
    """
       Table item with read-only property.

       This class represents a table item with read-only properties, which means the cell cannot be edited.

       Attributes
       ----------
       None

       Methods
       -------
       __init__(self, item)
           Initialize the CellItem with the provided item.

       Notes
       -----
       Inherits from QTableWidgetItem.

       Parameters
       ----------
       item : object
           The item to be displayed in the cell.

       Examples
       --------
       cell = CellItem("Read-only Text")
       tableWidget.setItem(0, 0, cell)

       """

    def __init__(self, item):
        """
        Initialize the CellItem.

        Parameters
        ----------
        item : object
            The item to be displayed in the cell.

        """

        super().__init__(item)
        self.setFlags(Qt.NoItemFlags)


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    """
       A delegate for center-aligned table items.

       This delegate is used to ensure the text alignment of table items is centered.

       Attributes
       ----------
       None

       Methods
       -------
       initStyleOption(option, index)
           Initialize the style options for the table items.

       Notes
       -----
       Inherits from QtWidgets.QStyledItemDelegate.

       Examples
       --------
       delegate = AlignDelegate()
       tableView.setItemDelegate(delegate)

       """

    def initStyleOption(self, option, index):
        """
        Initialize the style options for the table items.

        Parameters
        ----------
        option : QStyleOptionViewItem
            Style options for the item.
        index : QModelIndex
            Index of the item in the table.

        """

        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
