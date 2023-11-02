from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QToolButton, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QLabel

from .AutoSegmentationButton import AutoSegmentationButton
from .ClearButton import ClearButton
from .ColorMapButton import ColorMapButton
from .KernelButton import KernelButton
from .OverlayButton import OverlayButton
from .PlayButton import PlayButton
from .SaveButton import SaveButton
from .SaveTextBox import SaveTextBox


class Toolbar(QWidget):
    """
    A custom QWidget representing a toolbar with various tool buttons for image processing.

    Parameters
    ----------
    mainWindow : QWidget
        The main window widget to which the toolbar belongs.

    Attributes
    ----------
    centralFrame : QFrame
        The central frame containing all the tool buttons and labels.

    imageFrame : QFrame
        Frame containing image-related buttons and label.

    imageLabel : Label
        Label displaying "SERIES" text.

    playBtn : PlayButton
        Button for playing the image series.

    colorMapBtn : ColorMapButton
        Button for selecting color maps for the image.

    overlayBtn : OverlayButton
        Button for overlaying images.

    autoSegBtn : AutoSegmentationButton
        Button for automatic segmentation.

    clearBtn : ClearButton
        Button for clearing the current selection.

    maskFrame : QFrame
        Frame containing mask-related buttons and label.

    maskLabel : Label
        Label displaying "MASK" text.

    kernelBtn : KernelButton
        Button for drawing on the mask.

    analysisFrame : QFrame
        Frame containing analysis-related buttons and label.

    saveBtn : SaveButton
        Button for saving the output.

    saveTxtBox : SaveTextBox
        Text box for entering save file name.

    """

    def __init__(self, mainWindow):
        """
        Initialize the Toolbar widget.

        Parameters
        ----------
        mainWindow : QWidget
            The main window widget to which the toolbar belongs.

        """

        super().__init__(mainWindow)

        self.initUI()

    def initUI(self):
        """
        Initialize the user interface components and layout for the toolbar.

        """

        self.centralFrame = QFrame(self)
        self.centralFrame.setFixedHeight(39)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)

        self.imageFrame = QFrame(self.centralFrame)
        self.imageFrame.setFrameShape(QFrame.NoFrame)
        self.imageFrame.setFrameShadow(QFrame.Raised)
        self.imageFrame.setContentsMargins(5, 0, 0, 0)
        self.imageFrame.setStyleSheet("border: none;")

        # self.imageLabelFrame = QFrame(self.imageFrame)
        # self.imageLabelFrame.setFrameShape(QFrame.NoFrame)
        # self.imageLabelFrame.setFrameShadow(QFrame.Raised)
        # self.imageLabelFrame.setContentsMargins(0, 0, 0, 0)
        #
        # self.imageLabel = Label(self.imageLabelFrame)
        # self.imageLabel.setText("SERIES")
        #
        # self.imageLabelLayout = QHBoxLayout(self.imageLabelFrame)
        # self.imageLabelLayout.setContentsMargins(0, 0, 0, 0)
        # self.imageLabelLayout.addWidget(self.imageLabel)

        self.imageBtnsFrame = QFrame(self.imageFrame)
        self.imageBtnsFrame.setFrameShape(QFrame.NoFrame)
        self.imageBtnsFrame.setFrameShadow(QFrame.Raised)
        self.imageBtnsFrame.setContentsMargins(0, 0, 0, 0)

        self.playBtn = PlayButton(self.imageBtnsFrame)
        self.playBtn.setIconSize(QSize(30, 30))
        self.setButtonStyleSheet(self.playBtn)

        self.colorMapBtn = ColorMapButton(self.imageBtnsFrame)
        self.colorMapBtn.setIconSize(QSize(30, 30))
        self.setButtonStyleSheet(self.colorMapBtn)

        self.overlayBtn = OverlayButton(self.imageBtnsFrame)
        self.overlayBtn.setIconSize(QSize(30, 30))
        self.setButtonStyleSheet(self.overlayBtn)

        # self.autoSegBtn = AutoSegmentationButton(self.imageBtnsFrame)
        # self.autoSegBtn.setIconSize(QSize(30, 30))
        # self.setButtonStyleSheet(self.autoSegBtn)

        self.clearBtn = ClearButton(self.imageBtnsFrame)
        self.clearBtn.setIconSize(QSize(30, 30))
        self.setButtonStyleSheet(self.clearBtn)

        self.kernelBtn = KernelButton(self.imageBtnsFrame)
        self.kernelBtn.setIconSize(QSize(30, 30))
        self.kernelBtn.setToolTip("Draw on Mask")
        self.setButtonStyleSheet(self.kernelBtn)

        self.saveBtn = SaveButton(self.imageBtnsFrame)
        self.saveBtn.setIconSize(QSize(30, 30))
        self.saveBtn.setToolTip("Save Output")
        self.setButtonStyleSheet(self.saveBtn)

        self.imageBtnsLayout = QHBoxLayout(self.imageBtnsFrame)
        self.imageBtnsLayout.setContentsMargins(0, 0, 0, 0)
        self.imageBtnsLayout.addWidget(self.playBtn)
        self.imageBtnsLayout.addWidget(self.colorMapBtn)
        self.imageBtnsLayout.addWidget(self.overlayBtn)
        # self.imageBtnsLayout.addWidget(self.autoSegBtn)
        self.imageBtnsLayout.addWidget(self.clearBtn)
        self.imageBtnsLayout.addWidget(self.kernelBtn)
        self.imageBtnsLayout.addWidget(self.saveBtn)

        self.imageLayout = QHBoxLayout(self.imageFrame)
        self.imageLayout.setContentsMargins(0, 0, 0, 0)
        # self.imageLayout.addWidget(self.imageLabelFrame)
        self.imageLayout.addWidget(self.imageBtnsFrame)

        # self.separator1Frame = QFrame(self.centralFrame)
        # self.separator1Frame.setFrameShape(QFrame.VLine)
        # self.separator1Frame.setFixedWidth(1)
        #
        # self.separator1Layout = QHBoxLayout(self.separator1Frame)

        # self.maskFrame = QFrame(self.centralFrame)
        # self.maskFrame.setFrameShape(QFrame.NoFrame)
        # self.maskFrame.setFrameShadow(QFrame.Raised)
        # self.maskFrame.setContentsMargins(0, 0, 0, 0)
        # self.maskFrame.setStyleSheet("border: none;")
        #
        # self.maskLabelFrame = QFrame(self.maskFrame)
        # self.maskLabelFrame.setFrameShape(QFrame.NoFrame)
        # self.maskLabelFrame.setFrameShadow(QFrame.Raised)
        # self.maskLabelFrame.setContentsMargins(0, 0, 0, 0)

        # self.maskLabel = Label(self.maskLabelFrame)
        # self.maskLabel.setText("MASK")
        #
        # self.maskLabelLayout = QHBoxLayout(self.maskLabelFrame)
        # self.maskLabelLayout.addWidget(self.maskLabel)
        # self.maskLabelLayout.setContentsMargins(0, 0, 0, 0)

        # self.maskBtnsFrame = QFrame(self.maskFrame)
        # self.maskBtnsFrame.setFrameShape(QFrame.NoFrame)
        # self.maskBtnsFrame.setFrameShadow(QFrame.Raised)
        # self.maskBtnsFrame.setContentsMargins(0, 0, 0, 0)

        # self.kernelBtn = KernelButton(self.maskBtnsFrame)
        # self.kernelBtn.setIconSize(QSize(30, 30))
        # self.kernelBtn.setToolTip("Draw on Mask")
        # self.setButtonStyleSheet(self.kernelBtn)

        # self.maskBtnsLayout = QHBoxLayout(self.maskBtnsFrame)
        # self.maskBtnsLayout.addWidget(self.kernelBtn)
        # self.maskBtnsLayout.setContentsMargins(0, 0, 0, 0)

        # self.maskLayout = QHBoxLayout(self.maskFrame)
        # self.maskLayout.setContentsMargins(0, 0, 0, 0)
        # self.maskLayout.addWidget(self.maskLabelFrame)
        # self.maskLayout.addWidget(self.maskBtnsFrame)

        # self.separator2Frame = QFrame(self.centralFrame)
        # self.separator2Frame.setFrameShape(QFrame.VLine)
        # self.separator2Frame.setFixedWidth(1)
        #
        # self.separator2Layout = QHBoxLayout(self.separator2Frame)

        # self.analysisFrame = QFrame(self.centralFrame)
        # self.analysisFrame.setFrameShape(QFrame.NoFrame)
        # self.analysisFrame.setFrameShadow(QFrame.Raised)
        # self.analysisFrame.setContentsMargins(0, 0, 0, 0)
        # self.analysisFrame.setStyleSheet("border: none;")
        #
        # self.analysisLabelFrame = QFrame(self.analysisFrame)
        # self.analysisLabelFrame.setFrameShape(QFrame.NoFrame)
        # self.analysisLabelFrame.setFrameShadow(QFrame.Raised)
        # self.analysisLabelFrame.setContentsMargins(0, 0, 0, 0)
        #
        # self.analysisLabel = Label(self.analysisLabelFrame)
        # self.analysisLabel.setText("ANALYSIS")
        #
        # self.analysisLabelLayout = QHBoxLayout(self.analysisLabelFrame)
        # self.analysisLabelLayout.setContentsMargins(0, 0, 0, 0)
        # self.analysisLabelLayout.addWidget(self.analysisLabel)
        #
        # self.analysisBtnsFrame = QFrame(self.analysisFrame)
        # self.analysisBtnsFrame.setFrameShape(QFrame.NoFrame)
        # self.analysisBtnsFrame.setFrameShadow(QFrame.Raised)
        # self.analysisBtnsFrame.setContentsMargins(0, 0, 0, 0)
        #
        # self.saveBtn = SaveButton(self.analysisBtnsFrame)
        # self.saveBtn.setIconSize(QSize(30, 30))
        # self.saveBtn.setToolTip("Save Output")
        # self.setButtonStyleSheet(self.saveBtn)
        #
        # self.analysisBtnsLayout = QHBoxLayout(self.analysisBtnsFrame)
        # self.analysisBtnsLayout.addWidget(self.saveBtn)
        # self.analysisBtnsLayout.setContentsMargins(0, 0, 0, 0)
        #
        # self.analysisTxtBoxFrame = QFrame(self.analysisFrame)
        # self.analysisTxtBoxFrame.setFrameShape(QFrame.NoFrame)
        # self.analysisTxtBoxFrame.setFrameShadow(QFrame.Raised)
        # self.analysisTxtBoxFrame.setContentsMargins(0, 0, 0, 0)
        #
        # self.saveTxtBox = SaveTextBox(self.analysisTxtBoxFrame)
        # self.saveTxtBox.setFixedSize(150, 25)
        #
        # self.analysisTxtBoxLayout = QHBoxLayout(self.analysisTxtBoxFrame)
        # self.analysisTxtBoxLayout.addWidget(self.saveTxtBox)
        # self.analysisTxtBoxLayout.setContentsMargins(0, 0, 0, 0)
        #
        # self.analysisLayout = QHBoxLayout(self.analysisFrame)
        # self.analysisLayout.setContentsMargins(0, 0, 0, 0)
        # self.analysisLayout.addWidget(self.analysisLabelFrame)
        # self.analysisLayout.addWidget(self.analysisTxtBoxFrame)
        # self.analysisLayout.addWidget(self.analysisBtnsFrame)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.imageFrame)
        # self.centralLayout.addWidget(self.separator1Frame)
        # self.centralLayout.addWidget(self.maskFrame)
        # self.centralLayout.addWidget(self.separator2Frame)
        # self.centralLayout.addWidget(self.analysisFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.centralLayout.setAlignment(Qt.AlignLeft)
        self.centralLayout.setSpacing(10)

        self.uiLayout = QVBoxLayout(self)
        self.uiLayout.addWidget(self.centralFrame)
        self.uiLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.uiLayout)
        self.setContentsMargins(0, 0, 0, 0)

        self.setDisabled(True)

        self.centralFrame.setStyleSheet(
            "background-color: rgb(27, 29, 35);"
            "border: 1px solid gray;"
            "border-radius: 5px;")

    def seriesSelected(self, series):
        """
        Enable or disable tool buttons based on whether an active series is provided.

        Parameters
        ----------
        series : object
            The series object.

        Returns
        -------
        None

        """

        if series is None:
            self.setDisabled(True)

        elif series.parentSequence.getSeriesByType("Phase") is None:
            self.setDisabled(True)

        else:
            self.setDisabled(False)

        # self.saveTxtBox.setDefaultText()

    def setButtonStyleSheet(self, toolBtn):
        """
         Set the style sheet for the given tool button.

         Parameters
         ----------
         toolBtn : QToolButton
             The tool button to set the style sheet for.

         Returns
         -------
         None

         """

        toolBtn.setStyleSheet(u"QToolButton {"
                              "border: none;"
                              "background-color: transparent;"
                              "}"
                              "QToolButton:hover {"
                              "background-color: rgb(85, 170, 255);"
                              "}"
                              "QToolButton:pressed {"
                              "background-color: rgb(85, 170, 255);"
                              "}"
                              "QToolTip {"
                              "color:white;"
                              "background-color: black;"
                              "border: black solid 1px;"
                              "}")


class ToolButton(QToolButton):
    """
    Custom QToolButton representing a tool button in the toolbar.

    Parameters
    ----------
    parent : QWidget
        The parent widget for the tool button.

    """

    def __init__(self, parent):
        """
        Initialize the ToolButton widget.

        Parameters
        ----------
        parent : QWidget
            The parent widget for the tool button.

        """

        super().__init__(parent)

        self.initUI()

    def initUI(self):
        """
        Initialize the user interface components and layout for the tool button.

        """

        pass


class Label(QLabel):
    """
    Custom QLabel representing a label in the toolbar.

    Parameters
    ----------
    parent : QWidget
        The parent widget for the label.

    """

    def __init__(self, parent):
        """
        Initialize the Label widget.

        Parameters
        ----------
        parent : QWidget
            The parent widget for the label.

        """

        super().__init__(parent)

        self.initUI()

    def initUI(self):
        """
        Initialize the user interface components and layout for the label.

        """

        self.setContentsMargins(0, 0, 0, 0)
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)
