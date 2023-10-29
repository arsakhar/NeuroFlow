from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget, QSizeGrip

from ..Helper.Resources import *


class StatusBar(QWidget):
    """
    Custom status bar widget displaying developer information, application version, and a size grip for window resizing.

    Attributes
    ----------
    developerLabel : QLabel
        QLabel displaying the developer's name.

    instituteLabel : QLabel
        QLabel displaying the institute's name.

    universityLabel : QLabel
        QLabel displaying the university's name.

    versionLabel : QLabel
        QLabel displaying the application version.

    sizegrip : QSizeGrip
        QSizeGrip widget for window resizing.

    gripLabel : QLabel
        QLabel displaying the grip icon for window resizing.

    Methods
    -------
    __init__(self, parent)
        Constructs the StatusBar object.

    initUI(self)
        Initializes the user interface components and layouts.

    """

    def __init__(self, parent):
        """
        Constructs the StatusBar object.

        Parameters
        ----------
        parent : QWidget
            The parent widget of the StatusBar.

        """

        super().__init__()

        self.parent = parent

        self.initUI()

    def initUI(self):
        """
        Initializes the user interface components and layouts.

        """

        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setMinimumSize(QSize(0, 25))
        self.centralFrame.setMaximumSize(QSize(16777215, 25))
        self.centralFrame.setStyleSheet(u"background-color: rgb(27, 29, 35);")

        self.labelsFrame = QFrame(self.centralFrame)
        self.labelsFrame.setFrameShape(QFrame.NoFrame)
        self.labelsFrame.setFrameShadow(QFrame.Raised)
        self.labelsFrame.setContentsMargins(0, 0, 0, 0)
        self.labelsFrame.setStyleSheet("border: none;")

        self.developerLabel = Label(self.labelsFrame)
        self.developerLabel.setText("Ashwin Sakhare")

        self.instituteLabel = Label(self.labelsFrame)
        self.instituteLabel.setText("Stevens Neuroimaging and Informatics Institute")

        self.universityLabel = Label(self.labelsFrame)
        self.universityLabel.setText("University of Southern California")

        self.labelsLayout = QHBoxLayout(self.labelsFrame)
        self.labelsLayout.addWidget(self.developerLabel)
        self.labelsLayout.addWidget(self.instituteLabel)
        self.labelsLayout.addWidget(self.universityLabel)
        self.labelsLayout.setSpacing(50)
        self.labelsLayout.setContentsMargins(10, 0, 0, 0)
        self.labelsLayout.setAlignment(Qt.AlignLeft)

        self.versionFrame = QFrame(self.centralFrame)
        self.versionFrame.setFrameShape(QFrame.NoFrame)
        self.versionFrame.setFrameShadow(QFrame.Raised)
        self.versionFrame.setContentsMargins(0, 0, 0, 0)
        self.versionFrame.setStyleSheet("border: none;")

        self.versionLabel = Label(self.labelsFrame)
        self.versionLabel.setText("v1.0.0 alpha")

        self.versionLayout = QHBoxLayout(self.versionFrame)
        self.versionLayout.addWidget(self.versionLabel)
        self.versionLayout.setAlignment(Qt.AlignRight)
        self.versionLayout.setContentsMargins(0, 0, 20, 0)

        self.gripFrame = QFrame(self.centralFrame)
        self.gripFrame.setFrameShape(QFrame.NoFrame)
        self.gripFrame.setFrameShadow(QFrame.Raised)
        self.gripFrame.setMaximumSize(QSize(20, 20))
        self.gripFrame.setContentsMargins(0, 0, 0, 0)

        self.sizegrip = QSizeGrip(self.gripFrame)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        self.gripLabel = QLabel(self.gripFrame)
        self.pixmap = QPixmap(resource_path('icons/16x16/cil-size-grip.png'))
        self.gripLabel.setPixmap(self.pixmap)

        self.gripLayout = QHBoxLayout(self.gripFrame)
        self.gripLayout.addWidget(self.gripLabel)
        self.gripLayout.setAlignment(Qt.AlignCenter)
        self.gripLayout.setContentsMargins(0, 0, 0, 0)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.labelsFrame)
        self.centralLayout.addWidget(self.versionFrame)
        self.centralLayout.addWidget(self.gripFrame)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.uiLayout = QHBoxLayout(self)
        self.uiLayout.addWidget(self.centralFrame)
        self.uiLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.uiLayout)


class Label(QLabel):
    """
    Custom QLabel widget with specific font and style settings.

    Methods
    -------
    __init__(self, parent)
        Constructs the Label object.

    initUI(self)
        Initializes the user interface components and layouts.

    """

    def __init__(self, parent):
        """
        Constructs the Label object.

        Parameters
        ----------
        parent : QWidget
            The parent widget of the Label.

        """

        super().__init__(parent)

        self.initUI()

    def initUI(self):
        """
        Initializes the user interface components and layouts.

        """

        font = QFont()
        font.setFamily(u"Segoe UI")

        self.setFont(font)
        self.setStyleSheet(u"color: rgb(98, 103, 111);")
