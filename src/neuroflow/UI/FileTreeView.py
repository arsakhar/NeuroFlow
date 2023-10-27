from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon

from ..DICOM.DICOMReader import DICOMReader
from ..DICOM.Patient import Patient
from ..Helper.Resources import *


"""
Widget used as a container for the file system and tree view.
"""
class FileTreeView(QWidget):
    patientLoaded = pyqtSignal(Patient)

    def __init__(self, parent):
        super().__init__()

        self.workingDir = appSettings.value('dirPath', '')
        self.rootDir = ''

        self.fileExtensionFilters = ['*.DCM', '*.IMA']
        self.dicomDirFilter = 'DICOMDIR'
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
        self.model.setNameFilters(self.fileExtensionFilters + [self.dicomDirFilter])
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
        self.workingDir = self.model.filePath(self.tree.currentIndex())

        if not os.path.isdir(self.workingDir):
            self.workingDir = os.path.dirname(self.workingDir)

        workingIndex = self.model.index(self.workingDir)

        self.tree.setRootIndex(workingIndex)
        self.model.setRootPath(self.workingDir)

        self.activeDir = self.workingDir

        appSettings.setValue("dirPath", self.workingDir)

    def setRootLevel(self):
        self.tree.setRootIndex(self.model.index(self.rootDir))
        self.model.setRootPath(self.rootDir)

        self.activeDir = self.rootDir

    def checkSelection(self):
        filePath = self.model.filePath(self.tree.currentIndex())

        if os.path.isdir(filePath):
            return

        if not os.path.isfile(filePath):
            return

        fileName = os.path.basename(filePath)

        if fileName == self.dicomDirFilter:
            self.openDICOMDir(filePath)

        # elif any(extension in fileName for extension in self.imageFilters):
        #     self.parseDir(os.path.dirname(filePath))

        else:
            return

        self.activeDir = os.path.dirname(filePath)

    """
    Opens selected DICOMDir file.
    ================== ===========================================================================
    **Arguments:**
    index              tree double clicked event returns an index. index can then be 
                       converted to filepath
    
    **Signal:**
    patientLoaded      returns patient
    ================== ===========================================================================
    """
    def openDICOMDir(self, DICOMDirPath):
        if os.path.isfile(DICOMDirPath):
            self.dicomReader = DICOMReader()

            patient = self.dicomReader.load_patient_record(DICOMDirPath)

            if patient is None:
                return

            self.patientLoaded.emit(patient)

            # self.activeDir = os.path.dirname(DICOMDirPath)

    def parseDir(self, dirPath):
        if os.path.isdir(dirPath):
            self.dicomReader = DICOMReader()

            patient = self.dicomReader.try_parse_dir(dirPath)

            if patient is None:
                return

            self.patientLoaded.emit(patient)

            # self.activeDir = dirPath

    def resizeEvent(self, event):
        self.tree.resize(self.frameGeometry().width(), self.frameGeometry().height())
        self.tree.adjustColumnWidths()


"""
Creates a QFileSystemModel. This is along with QTreeView creates a file system that can be browsed within the widget.
"""
class FileSystemModel(QFileSystemModel):
    def __init__(self, parent):
        super().__init__(parent)

        self.setNameFilterDisables(False)


"""
Creates a QTreeView. This is used to display the file system tree.
"""
class TreeView(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.setAnimated(False)
        self.setIndentation(20)
        self.setSortingEnabled(True)

        self.initUI()

    def initUI(self):
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
        self.setColumnWidth(0, int(self.frameGeometry().width() * .5))
        self.setColumnWidth(1, int(self.frameGeometry().width() * .1))
        self.setColumnWidth(2,  int(self.frameGeometry().width() * .2))
        self.setColumnWidth(3, int(self.frameGeometry().width() * .2 - 5))

    def setStyleSheet(self):
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
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
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

