from pathlib import Path
from typing import Union

from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QFrame

from ..DICOM.DICOMReader import DICOMReader
from ..DICOM.Patient import Patient
from ..Helper.Resources import *


class FileTreeView(QWidget):
    """
    A widget to display a file tree view and handle directory selection events.

    Parameters
    ----------
    parent : QWidget
        The parent widget for this FileTreeView.

    Signals
    -------
    patientLoaded : pyqtSignal
        Signal emitted when a patient is loaded. The signal carries a Patient object.

    Attributes
    ----------
    workingDir : str
        The current working directory path.

    rootDir : str
        The root directory path.

    fileExtensionFilters : list of str
        List of file extensions to filter files in the tree view.

    dicomdirFilter : str
        Filter for DICOM directories.

    imageFilters : list of str
        List of supported image file formats.

    model : FileSystemModel
        File system model for the tree view.

    tree : TreeView
        Tree view widget displaying the file system.

    rootBtn : MenuButton
        Button to go to the root directory.

    workingBtn : MenuButton
        Button to set the working directory.

    openBtn : MenuButton
        Button to open a selected patient's data.

    activeDir : str
        The currently active directory path.
    """

    patientLoaded = pyqtSignal(object)

    def __init__(self, parent):
        """
        Initializes the FileTreeView widget.

        Parameters
        ----------
        parent : QWidget
            The parent widget.

        """

        super().__init__()

        self.parent = parent

        self.workingDir = appSettings.value('dirPath', '')
        self.rootDir = ''

        self.fileExtensionFilters = ['*.DCM', '*.IMA']
        self.dicomdirFilter = 'DICOMDIR'
        self.imageFilters = ['DCM', 'IMA']

        self.model = None
        self.tree = None

        self.rootBtn = None
        self.workingBtn = None
        self.openBtn = None

        self.activeDir = None

        self.initUI()

        self.tree.doubleClicked.connect(self.checkSelection)
        self.rootBtn.clicked.connect(self.setRootLevel)
        self.workingBtn.clicked.connect(self.setWorkingLevel)
        self.openBtn.clicked.connect(self.checkSelection)

    def initUI(self):
        """
        Initializes the user interface of the FileTreeView widget.

        """

        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.menuFrame = QFrame(self.centralFrame)
        self.menuFrame.setFrameShape(QFrame.NoFrame)
        self.menuFrame.setFrameShadow(QFrame.Raised)
        self.menuFrame.setContentsMargins(0, 0, 0, 0)
        self.menuFrame.setStyleSheet("background-color: rgb(15, 15, 15);")

        self.rootBtn = MenuButton(self.menuFrame)
        self.rootBtn.setIcon(QIcon(resource_path("icons/16x16/cil-home")))
        self.rootBtn.setToolTip("Go To Root Directory")

        self.workingBtn = MenuButton(self.menuFrame)
        self.workingBtn.setIcon(QIcon(resource_path("icons/16x16/cil-briefcase")))
        self.workingBtn.setToolTip("Set Working Directory")

        self.openBtn = MenuButton(self.menuFrame)
        self.openBtn.setIcon(QIcon(resource_path("icons/16x16/cil-folder-open")))
        self.openBtn.setToolTip("Open Patient")

        self.menuLayout = QHBoxLayout(self.menuFrame)
        self.menuLayout.addWidget(self.rootBtn)
        self.menuLayout.addWidget(self.workingBtn)
        self.menuLayout.addWidget(self.openBtn)
        self.menuLayout.setContentsMargins(2, 2, 2, 2)
        self.menuLayout.setAlignment(Qt.AlignLeft)
        self.menuLayout.setSpacing(10)

        self.treeFrame = QFrame(self.centralFrame)
        self.treeFrame.setFrameShape(QFrame.NoFrame)
        self.treeFrame.setFrameShadow(QFrame.Raised)
        self.treeFrame.setContentsMargins(0, 0, 0, 0)
        self.treeFrame.setStyleSheet("border: none;")

        self.model = FileSystemModel(self.treeFrame)
        self.model.setNameFilters(self.fileExtensionFilters + [self.dicomdirFilter])
        self.model.setNameFilterDisables(False)
        self.model.setRootPath(self.workingDir)

        self.tree = TreeView(self.treeFrame)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.workingDir))
        self.tree.resize(self.frameGeometry().width(), self.frameGeometry().height())
        self.tree.adjustColumnWidths()
        self.tree.setContentsMargins(0, 0, 0, 0)

        self.treeLayout = QVBoxLayout(self.treeFrame)
        self.treeLayout.addWidget(self.tree)
        self.treeLayout.setContentsMargins(0, 0, 0, 0)
        self.treeLayout.setSpacing(0)

        self.centralLayout = QVBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.menuFrame, stretch=1)
        self.centralLayout.addWidget(self.treeFrame, stretch=10)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)

    def setWorkingLevel(self):
        """
        Sets the working directory level based on the selected item in the tree view.

        """

        self.workingDir = self.model.filePath(self.tree.currentIndex())

        if not os.path.isdir(self.workingDir):
            self.workingDir = os.path.dirname(self.workingDir)

        workingIndex = self.model.index(self.workingDir)

        self.tree.setRootIndex(workingIndex)
        self.model.setRootPath(self.workingDir)

        self.activeDir = self.workingDir

        appSettings.setValue("dirPath", self.workingDir)

    def setRootLevel(self):
        """
        Sets the root directory level in the tree view.

        """

        self.tree.setRootIndex(self.model.index(self.rootDir))
        self.model.setRootPath(self.rootDir)

        self.activeDir = self.rootDir

    def checkSelection(self):
        """
        Checks the selected item in the tree view and opens DICOM directories or image files.

        """

        filepath = Path(self.model.filePath(self.tree.currentIndex()))

        if not filepath.is_file():
            return

        if filepath.name == self.dicomdirFilter:
            self.openDICOMDIR(filepath)

        else:
            return

        self.activeDir = os.path.dirname(filepath)

    def openDICOMDIR(self, filepath: Union[str, Path]):
        """
        Opens the selected DICOM directory and emits the patientLoaded signal.

        Parameters
        ----------
        filepath : Union[str, Path]
            Path to the selected DICOM directory.

        """

        filepath = Path(filepath)

        if filepath.is_file():
            self.dicomdir_reader = DICOMReader()

            patient = self.dicomdir_reader.load_patient_record(filepath)

            if patient is None:
                return

            self.patientLoaded.emit(patient)

    def resizeEvent(self, event):
        """
        Overrides the resizeEvent method to adjust the tree view's size.

        Parameters
        ----------
        event : QResizeEvent
            The resize event.

        """

        self.tree.resize(self.frameGeometry().width(), self.frameGeometry().height())
        self.tree.adjustColumnWidths()


class FileSystemModel(QFileSystemModel):
    """
    Custom QFileSystemModel class to handle file system operations.

    """

    def __init__(self, parent):
        """
        Initializes the FileSystemModel.

        Parameters
        ----------
        parent : QWidget
            The parent widget.

        """

        super().__init__(parent)

        self.setNameFilterDisables(False)


class TreeView(QTreeView):
    """
    Custom QTreeView class for displaying the file system tree.

    This class extends QTreeView to create a customized tree view widget for displaying the file system.
    It includes specific styles and column width adjustments.

    Parameters
    ----------
    parent : QWidget
       The parent widget.

    Attributes
    ----------
    parent : QWidget
       The parent widget.

    centralFrame : QFrame
       Frame widget to hold the tree view.

    centralLayout : QVBoxLayout
       Layout for the central frame.

    Methods
    -------
    initUI()
       Initializes the user interface of the TreeView widget.

    adjustColumnWidths()
       Adjusts the column widths of the tree view based on the widget's geometry.

    setStyleSheet()
       Sets the custom style sheet for the tree view.

    """

    def __init__(self, parent):
        """
        Initializes the TreeView.

        Parameters
        ----------
        parent : QWidget
            The parent widget.

        """

        super().__init__(parent)

        self.parent = parent

        self.setAnimated(False)
        self.setIndentation(20)
        self.setSortingEnabled(True)

        self.initUI()

    def initUI(self):
        """
        Initializes the user interface of the TreeView widget.

        This method sets up the central frame and layout for the tree view.

        """

        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.centralLayout = QVBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.centralFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)
        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet()

    def adjustColumnWidths(self):
        """
        Adjusts the column widths of the tree view.

        This method adjusts the column widths based on the width of the widget.

        """

        self.setColumnWidth(0, int(self.frameGeometry().width() * .5))
        self.setColumnWidth(1, int(self.frameGeometry().width() * .1))
        self.setColumnWidth(2,  int(self.frameGeometry().width() * .2))
        self.setColumnWidth(3, int(self.frameGeometry().width() * .2 - 5))

    def setStyleSheet(self):
        """
        Adjusts the column widths of the tree view.

        """

        super().setStyleSheet("QTreeView::item{\n"
                              "	border-color: rgb(44, 49, 60);\n"
                              "	padding-left: 5px;\n"
                              "	padding-right: 5px;\n"
                              "	gridline-color: rgb(44, 49, 60);\n"
                              "}\n"
                              "QTreeView::item:selected{\n"
                              "	background-color: rgb(85, 170, 255);\n"
                              "}\n"
                              "QTreeView::branch:selected{\n"
                              "	background-color: rgb(85, 170, 255);\n"
                              "}\n"
                              "QHeaderView::section{\n"
                              "	Background-color: rgb(39, 44, 54);\n"
                              "	max-width: 30px;\n"
                              "	border: 1px solid rgb(44, 49, 60);\n"
                              "	border-style: none;\n"
                              "    border-bottom: 1px solid rgb(44, 49, 60);\n"
                              "    border-right: 1px solid rgb(44, 49, 60);\n"
                              "}\n"
                              ""
                              "QTreeView::horizontalHeader {	\n"
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


class MenuButton(QPushButton):
    """
    Custom QPushButton class for menu buttons.

    This class extends QPushButton to create customized menu buttons with specific styles.

    Parameters
    ----------
    parent : QWidget
       The parent widget.

    Attributes
    ----------
    None

    Methods
    -------
    initUI()
       Initialize the appearance and behavior of the MenuButton.

    """

    def __init__(self, parent):
        """
        Initializes the MenuButton.

        Parameters
        ----------
        parent : QWidget
            The parent widget.

        """

        super().__init__(parent)

        self.initUI()

    def initUI(self):
        """
        Initialize the appearance and behavior of the MenuButton.

        The MenuButton is styled with specific properties for normal, hover, and pressed states.
        Additionally, tooltips are styled to have white text on a black background with a black border.

        """

        self.setIconSize(QSize(20, 20))

        self.setStyleSheet(u"QPushButton {"
                           "border: none;"
                           "background-color: transparent;"
                           "}"
                           "QPushButton:hover {"
                           "background-color: rgb(85, 170, 255);"
                           "}"
                           "QPushButton:pressed {"
                           "background-color: rgb(85, 170, 255);"
                           "}"
                           "QToolTip {"
                           "color:white;"
                           "background-color: black;"
                           "border: black solid 1px;"
                           "}")

