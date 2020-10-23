from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from scripts.UI.Cursor import Cursor
# from scripts.ML.LevelClassification import LevelClassification


class ImageStats(QWidget):
    def __init__(self, seriesGraphics):
        super().__init__(seriesGraphics)

        self.seriesGraphics = seriesGraphics
        self.viewBox = self.seriesGraphics.view

        self.initUI()

        self.viewBox.sigTransformChanged.connect(self.viewResized)
        self.viewBox.sigTransformChanged.connect(self.updateZoom)
        self.seriesGraphics.timeLine.sigPositionChanged.connect(self.updateImage)
        self.seriesGraphics.imageItem.mouseHovered.connect(self.updatePosition)
        self.seriesGraphics.imageItem.mouseHovered.connect(self.updateIntensity)

    def initUI(self):
        self.centralFrame = QFrame(self)

        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)

        self.centralLayout = QVBoxLayout(self.centralFrame)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.infoFrame = QFrame(self.centralFrame)
        self.infoFrame.setStyleSheet(u"background-color: rgb(27, 29, 35);")

        self.infoFrame.setFrameShape(QFrame.NoFrame)
        self.infoFrame.setFrameShadow(QFrame.Raised)
        self.infoFrame.setContentsMargins(0, 0, 0, 0)
        self.infoFrame.setMinimumHeight(0)

        self.imageFrame = QFrame(self.infoFrame)
        self.imageFrame.setFrameShape(QFrame.NoFrame)
        self.imageFrame.setFrameShadow(QFrame.Raised)
        self.imageFrame.setStyleSheet(u"border: none;")
        self.imageFrame.setContentsMargins(0, 0, 0, 0)

        self.imageLayout = QHBoxLayout(self.imageFrame)
        self.imageLayout.setContentsMargins(0, 0, 0, 0)
        self.imageLayout.setSpacing(1)

        self.imageLabel = Label(self.imageFrame)
        self.imageLabel.setText("Image: ")

        self.imageValue = Label(self.imageFrame)
        self.imageValue.setText("")

        self.imageLayout.addWidget(self.imageLabel)
        self.imageLayout.addWidget(self.imageValue)

        self.zoomFrame = QFrame(self.infoFrame)
        self.zoomFrame.setFrameShape(QFrame.NoFrame)
        self.zoomFrame.setFrameShadow(QFrame.Raised)
        self.zoomFrame.setStyleSheet(u"border: none;")
        self.zoomFrame.setContentsMargins(0, 0, 0, 0)

        self.zoomLayout = QHBoxLayout(self.zoomFrame)
        self.zoomLayout.setContentsMargins(0, 0, 0, 0)
        self.zoomLayout.setSpacing(1)

        self.zoomLabel = Label(self.zoomFrame)
        self.zoomLabel.setText("Zoom: ")

        self.zoomValue = Label(self.zoomFrame)
        self.zoomValue.setText("")

        self.zoomLayout.addWidget(self.zoomLabel)
        self.zoomLayout.addWidget(self.zoomValue)

        self.posFrame = QFrame(self.infoFrame)
        self.posFrame.setFrameShape(QFrame.NoFrame)
        self.posFrame.setFrameShadow(QFrame.Raised)
        self.posFrame.setStyleSheet(u"border: none;")
        self.posFrame.setContentsMargins(0, 0, 0, 0)

        self.posLayout = QHBoxLayout(self.posFrame)
        self.posLayout.setContentsMargins(0, 0, 0, 0)
        self.posLayout.setSpacing(1)

        self.posLabel = Label(self.posFrame)
        self.posLabel.setText("Pos: ")

        self.posValue = Label(self.posFrame)
        self.posValue.setText("")

        self.posLayout.addWidget(self.posLabel)
        self.posLayout.addWidget(self.posValue)

        self.intensityFrame = QFrame(self.infoFrame)
        self.intensityFrame.setFrameShape(QFrame.NoFrame)
        self.intensityFrame.setFrameShadow(QFrame.Raised)
        self.intensityFrame.setStyleSheet(u"border: none;")
        self.intensityFrame.setContentsMargins(0, 0, 0, 0)

        self.intensityLayout = QHBoxLayout(self.intensityFrame)
        self.intensityLayout.setContentsMargins(0, 0, 0, 0)
        self.intensityLayout.setSpacing(1)

        self.intensityLabel = Label(self.intensityFrame)
        self.intensityLabel.setText("Value: ")

        self.intensityValue = Label(self.intensityFrame)
        self.intensityValue.setText("")

        self.intensityLayout.addWidget(self.intensityLabel)
        self.intensityLayout.addWidget(self.intensityValue)

        self.levelFrame = QFrame(self.infoFrame)
        self.levelFrame.setFrameShape(QFrame.NoFrame)
        self.levelFrame.setFrameShadow(QFrame.Raised)
        self.levelFrame.setStyleSheet(u"border: none;")
        self.levelFrame.setContentsMargins(0, 0, 0, 0)

        self.levelLayout = QHBoxLayout(self.levelFrame)
        self.levelLayout.setContentsMargins(0, 0, 0, 0)
        self.levelLayout.setSpacing(1)

        self.levelLabel = Label(self.levelFrame)
        self.levelLabel.setText("Level: ")

        self.levelValue = Label(self.levelFrame)
        self.levelValue.setText("")

        self.levelLayout.addWidget(self.levelLabel)
        self.levelLayout.addWidget(self.levelValue)

        self.roiFrame = QFrame(self.infoFrame)
        self.roiFrame.setFrameShape(QFrame.NoFrame)
        self.roiFrame.setFrameShadow(QFrame.Raised)
        self.roiFrame.setStyleSheet(u"border: none;")
        self.roiFrame.setContentsMargins(0, 0, 0, 0)

        self.roiLayout = QHBoxLayout(self.roiFrame)
        self.roiLayout.setContentsMargins(0, 0, 0, 0)
        self.roiLayout.setSpacing(1)

        self.roiLabel = Label(self.roiFrame)
        self.roiLabel.setText("ROI: ")

        self.roiValue = Label(self.roiFrame)
        self.roiValue.setText("")

        self.roiLayout.addWidget(self.roiLabel)
        self.roiLayout.addWidget(self.roiValue)

        self.infoLayout = QHBoxLayout(self.infoFrame)
        self.infoLayout.setSpacing(10)
        self.infoLayout.setContentsMargins(0, 0, 0, 0)

        self.infoLayout.addWidget(self.imageFrame)
        self.infoLayout.addWidget(self.zoomFrame)
        self.infoLayout.addWidget(self.posFrame)
        self.infoLayout.addWidget(self.intensityFrame)
        self.infoLayout.addWidget(self.levelFrame)
        self.infoLayout.addWidget(self.roiFrame)

        self.infoLayout.setAlignment(Qt.AlignCenter)

        self.centralLayout.addWidget(self.infoFrame)
        self.centralLayout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.centralLayout)

        self.disable()

    """
    Called when mouse hovers over image information graphics box
    ================== ===========================================================================
    **Arguments:**
    ev                 the pyqt event
    ================== ===========================================================================
    """
    def enterEvent(self,ev):
        cursor = Cursor()
        self.setCursor(cursor.DefaultCursor)
        super().enterEvent(ev)

    """
    Called when this widget is resized. Resize box width to same as parent viewbox width
    """
    def viewResized(self):
        self.setFixedSize(self.viewBox.screenGeometry().width(), 35)

    """
    Shows widget
    Uncomment to use classification of level. It takes longer so i'm commenting out for now.
    """
    def enable(self):
        # levelClassification = LevelClassification()
        #
        # model = levelClassification.load_model()
        # level = levelClassification.predict(model=model, img=self.seriesGraphics.image)

        self.updateImage()
        # self.updateLevel(level)

        super().show()

    """
    Hides widget
    """
    def disable(self):
        super().hide()

    """
    Updates image text with current image index in series
    """
    def updateImage(self):
        self.imageValue.setText(str(self.seriesGraphics.currentIndex))

    """
    Updates zoom text with current zoom level on image
    """
    def updateZoom(self):
        maxHeight = self.viewBox.boundingRect().height()
        maxWidth = self.viewBox.boundingRect().width()

        maxRange = maxHeight if maxHeight < maxWidth else maxWidth

        widthRange = self.viewBox.viewRange()[0][1] - self.viewBox.viewRange()[0][0]
        heightRange = self.viewBox.viewRange()[1][1] - self.viewBox.viewRange()[1][0]

        currRange = heightRange if maxHeight < maxWidth else widthRange

        zoom = int(round(maxRange/ currRange))

        self.zoomValue.setText(str(zoom) + "x")

    """
    Updates position text with current mouse position in image
    """
    def updatePosition(self, ev):
        try:
            currPos = ev.pos()

            currPos = QtCore.QPointF(round(currPos.x()), round(currPos.y()))

        except:
            return

        currPos = str(int(currPos.x())) + ", " + str(int(currPos.y()))

        self.posValue.setText(currPos)

    """
    Updates intensity text with current pixel intensity at mouse position in image
    """
    def updateIntensity(self, ev):
        try:
            currPos = ev.pos()

            currPos = QtCore.QPointF(round(currPos.x()), round(currPos.y()))

        except:
            return

        intensity = self.seriesGraphics.image[self.seriesGraphics.currentIndex, int(currPos.x()), int(currPos.y())]

        self.intensityValue.setText(str(intensity))

    """
    Updates level text with predicted anatomical level
    """
    def updateLevel(self, level):
        self.levelValue.setText(str(level))


"""
Creates labels associated with text values defined above
"""
class Label(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        font = QFont()
        font.setFamily(u"Segoe UI")

        self.setFont(font)
        self.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.setContentsMargins(0, 0, 0, 0)
