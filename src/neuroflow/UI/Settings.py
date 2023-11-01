from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog,
                             QTableWidget, QTableWidgetItem, QFrame, QSizePolicy, QSpacerItem
                             )

from ..Helper.Resources import appSettings


class Settings(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.settingsFrame = QFrame(self.centralFrame)
        self.settingsFrame.setFrameShape(QFrame.NoFrame)
        self.settingsFrame.setFrameShadow(QFrame.Raised)
        self.settingsFrame.setContentsMargins(0, 0, 0, 0)
        self.settingsFrame.setStyleSheet("font-size: 14px;")

        self.saveFrame = QFrame(self.settingsFrame)
        self.saveFrame.setFrameShape(QFrame.NoFrame)
        self.saveFrame.setFrameShadow(QFrame.Raised)
        self.saveFrame.setContentsMargins(0, 0, 0, 0)

        self.saveLabel = QLabel(self.saveFrame)
        self.saveLabel.setText('Save Directory:')

        self.saveDir = QLineEdit(self.saveFrame)
        self.saveDir.setReadOnly(True)

        self.browseBtn = SetingsBtn(self.saveFrame)
        self.browseBtn.setText('Browse')
        self.browseBtn.setFixedWidth(self.browseBtn.width() + 10)

        # Save Directory Layout
        self.saveLayout = QHBoxLayout(self.saveFrame)
        self.saveLayout.addWidget(self.saveLabel)
        self.saveLayout.addWidget(self.saveDir)
        self.saveLayout.addWidget(self.browseBtn)

        self.labelFrame = QFrame(self.settingsFrame)
        self.labelFrame.setFrameShape(QFrame.NoFrame)
        self.labelFrame.setFrameShadow(QFrame.Raised)
        self.labelFrame.setContentsMargins(0, 0, 0, 0)

        self.labelTable = QTableWidget(self.labelFrame)
        self.labelTable.setColumnCount(1)
        self.labelTable.setHorizontalHeaderLabels(['Labels'])
        self.labelTable.setColumnWidth(0, self.labelTable.width() * 20)

        self.labelBtn = SetingsBtn(self.labelFrame)
        self.labelBtn.setText('Add Label')
        self.labelBtn.clicked.connect(self.addLabel)

        self.labelLayout = QVBoxLayout(self.labelFrame)
        self.labelLayout.addWidget(self.labelTable)
        self.labelLayout.addWidget(self.labelBtn)

        self.settingsLayout = QVBoxLayout(self.settingsFrame)
        self.settingsLayout.setContentsMargins(0, 0, 0, 0)
        self.settingsLayout.addWidget(self.saveFrame, alignment=Qt.AlignTop)
        self.settingsLayout.addWidget(self.labelFrame, alignment=Qt.AlignTop)

        self.spacerFrame = QFrame(self.centralFrame)
        self.spacerFrame.setFrameShape(QFrame.NoFrame)
        self.spacerFrame.setFrameShadow(QFrame.Raised)
        self.spacerFrame.setContentsMargins(0, 0, 0, 0)

        self.spacerLayout = QVBoxLayout(self.spacerFrame)
        self.spacerLayout.setContentsMargins(0, 0, 0, 0)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.centralLayout.addWidget(self.settingsFrame, stretch=1, alignment=Qt.AlignTop)
        self.centralLayout.addWidget(self.spacerFrame, stretch=1, alignment=Qt.AlignTop)

        self.uiLayout = QHBoxLayout(self)
        self.uiLayout.addWidget(self.centralFrame)
        self.uiLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.uiLayout)

        self.browseBtn.clicked.connect(self.openFileDialog)
        self.labelTable.itemChanged.connect(self.updateLabelAppSettings)

        self.loadSettings()

    def openFileDialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if not folder_path:
            return

        self.saveDir.setText(folder_path)
        appSettings.setValue("Save Directory", folder_path)

    def addLabel(self):
        rowPosition = self.labelTable.rowCount()
        self.labelTable.insertRow(rowPosition)

    def loadSettings(self):
        # Load selected directory from settings
        saved_directory = appSettings.value("Save Directory", "")
        if saved_directory and QDir(saved_directory).exists():
            self.saveDir.setText(saved_directory)

        # Load labels from settings
        saved_labels = appSettings.value("Labels", [])
        if not saved_labels:
            return

        for label in saved_labels:
            self.addLabelToTable(label)

    def addLabelToTable(self, label):
        rowPosition = self.labelTable.rowCount()
        self.labelTable.insertRow(rowPosition)
        label_item = QTableWidgetItem(label)
        self.labelTable.setItem(rowPosition, 0, label_item)

    def updateLabelAppSettings(self, item):
        labels = [self.labelTable.item(row, 0).text() for row in range(self.labelTable.rowCount())
                  if self.labelTable.item(row, 0) is not None
                  ]
        appSettings.setValue("Labels", labels)


class Table(QTableWidget):
    def __init__(self):
        super().__init__()


class SetingsBtn(QPushButton):
    """
    Custom QPushButton class for settings buttons.

    This class extends QPushButton to create customized menu buttons with specific styles.

    Parameters
    ----------
    parent : QWidget
       The parent widget.

    Attributes
    ----------
    None

    """

    def __init__(self, parent):
        """
        Initializes the SettingsBtn.

        Parameters
        ----------
        parent : QWidget
            The parent widget.

        """

        super().__init__(parent)

        self.initUI()

    def initUI(self):
        """
        Initialize the appearance and behavior of the SettingsBtn.

        The SettingsBtn is styled with specific properties for normal, hover, and pressed states.
        Additionally, tooltips are styled to have white text on a black background with a black border.

        """

        self.setStyleSheet(u"QPushButton {"
                           "border: none;"
                           "background-color: #444955;"
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
