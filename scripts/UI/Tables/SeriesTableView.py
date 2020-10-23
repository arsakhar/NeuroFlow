from PyQt5.QtWidgets import QFrame, QTableView, QVBoxLayout
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd


"""
Widget used to display data elements associated with a Series images.
https://pydicom.github.io/pydicom/0.9/pydicom_user_guide.html
"""
class SeriesTableView(QTableView):
    def __init__(self, parent):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.model = PandasModel(self.centralFrame)

        self.centralLayout = QVBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.centralFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)

        self.setStyleSheet()

    def newPatient(self, patient):
        self.model._data = None
        self.reset()

    """
    Populates a table view with data associated with an series
    ================== ===========================================================================
    **Arguments:**
    series             the series object
    ================== ===========================================================================
    """
    def seriesSelected(self, series):
        self.model._data = None
        self.reset()

        if series is None:
            return

        data = series.images[0].dataset  # let's pick the first image in the series to display

        dataElements = []

        dataElementHeaders = ['Tag', 'Description', 'VR', 'Value']

        dataElements = self.getDataElements(data, dataElements)

        data_df = pd.DataFrame(dataElements, columns=dataElementHeaders)

        self.model._data = data_df
        self.setModel(self.model)
        self.adjustColumnWidths()

        delegate = AlignDelegate(self)
        self.setItemDelegate(delegate)

    """
    Parses an image's dataset into data elements. Data elements are objects that store a tag,
    DICOM value representation (VR), value multiplicity (VM), and value (#, string, list, sequence)
    https://pydicom.github.io/pydicom/0.9/pydicom_user_guide.html#dataelement
    ================== ===========================================================================
    **Arguments:**
    data               image dataset
    dataElements       (optional) a list of data elements to append to
    
    **Returns:**
    dataElements       a list of data elements associated with image dataset
    ================== ===========================================================================
    """
    def getDataElements(self, data, dataElements=None):
        if dataElements is None:
            dataElements = []

        for dataElement in data:
            tag = str(dataElement.tag)
            tag = tag.strip()

            VR = dataElement.VR
            VR = VR.strip()

            value = str(dataElement.value)
            value = value.strip()

            description = str(dataElement)

            description = description.replace(tag, '')
            description = description.replace(VR, '')
            description = description.split(':', 1)[0]
            description = description.strip()

            dataElements.append([tag, description, VR, value])

        return dataElements

    def resizeEvent(self, ev):
        if self.model._data is None:
            return

        self.adjustColumnWidths()

    def adjustColumnWidths(self):
        proposedColWidth = ((self.frameGeometry().width() - 50) / self.model.columnCount())

        for column in range(0, self.model.columnCount()):
            minColWidth = self.sizeHintForColumn(column)

            if (proposedColWidth > minColWidth):
                self.setColumnWidth(column, proposedColWidth)

            else:
                self.setColumnWidth(column, minColWidth)

        self.horizontalHeader().setStretchLastSection(True)

    def setStyleSheet(self):
        super().setStyleSheet("QTableView::item{\n"
                              "	border-color: rgb(44, 49, 60);\n"
                              "	padding-left: 5px;\n"
                              "	padding-right: 5px;\n"
                              "	gridline-color: rgb(44, 49, 60);\n"
                              "}\n"
                              "QTableView::item:selected{\n"
                              "	background-color: rgb(85, 170, 255);\n"
                              "}\n"
                              "QTableView::section{\n"
                              "	Background-color: rgb(39, 44, 54);\n"
                              "	max-width: 30px;\n"
                              "	border: 1px solid rgb(44, 49, 60);\n"
                              "	border-style: none;\n"
                              "    border-bottom: 1px solid rgb(44, 49, 60);\n"
                              "    border-right: 1px solid rgb(44, 49, 60);\n"
                              "}\n"
                              ""
                              "QTableView::horizontalHeader {	\n"
                              "	background-color: rgb(81, 255, 0);\n"
                              "}\n"
                              "QHeaderView::section:horizontal\n"
                              "{\n"
                              "    border: 1px solid rgb(32, 34, 42);\n"
                              "	background-color: rgb(27, 29, 35);\n"
                              "	padding: 3px;\n"
                              "}\n"
                              "QHeaderView::section:vertical\n"
                              "{\n"
                              "    border: 1px solid rgb(44, 49, 60);\n"
                              "}\n"
                              "")


"""
Abstract Widget used to populate a table view from a pandas dataframe
"""
class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, parent):
        super().__init__(parent)
        self._data = None

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])

        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]

        return None


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
