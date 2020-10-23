from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QTabWidget, QStackedLayout, QFrame
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

from scripts.UI.Graphics.FlowGraphicsView import FlowGraphicsView
from scripts.UI.Tables.PatientTableView import PatientTableView
from scripts.UI.Toolbar.Toolbar import Toolbar
from scripts.UI.Tables.FlowTableView import FlowTableView
from scripts.UI.FileTreeView import FileTreeView
from scripts.UI.Tables.SeriesTableView import SeriesTableView
from scripts.UI.Graphics.SeriesGraphicsView import SeriesGraphicsView
from scripts.UI.Graphics.MaskGraphicsView import MaskGraphicsView
from scripts.UI.TitleBar import TitleBar
from scripts.UI.SideMenu import SideMenu
from scripts.UI.StatusBar import StatusBar
from scripts.Helper.Resources import *


"""
Widget containing the main window (everything the user sees)
"""
class MainWindow(QMainWindow):
    FILE_TREE_VIEW = 0
    SERIES_GRAPHICS_VIEW = 1
    SERIES_TABLE_VIEW = 2

    def __init__(self):
        super().__init__()

        # Instantiate Title Bar
        self.titleBar = TitleBar(self)

        # Instantiate Status Bar. Add grip to status bar to allow for resizing window
        self.statusBar = StatusBar(self)

        # Instantiate Side Menu
        self.sideMenu = SideMenu(self)

        # Instantiate Toolbar
        self.toolBar = Toolbar(self)

        # Instantiate File System Tab
        self.fileTreeView = FileTreeView(self)

        # Instantiate Patient Table
        self.patientTableView = PatientTableView(self)

        # Instantiate Mask Graphics
        self.maskGraphicsView = MaskGraphicsView(self, self.toolBar)

        # Instantiate Series Graphics
        self.seriesGraphicsView = SeriesGraphicsView(self, self.toolBar)

        # Instantiate Series Table
        self.seriesTableView = SeriesTableView(self)

        # Instantiate Flow Table
        self.flowTableView = FlowTableView(self, self.toolBar)

        # Instantiate Flow Graphics
        self.flowGraphicsView = FlowGraphicsView(self, self.toolBar)

        self.initUI()

        # self.sideMenu.homeBtn.clicked.connect(lambda: self.contentLayout.setCurrentIndex(
        #     self.sideMenu.HOME_BUTTON))

    def initUI(self):
        self.setWindowIcon(QtGui.QIcon(resource_path('icons/logo.png')))
        self.setObjectName("mainWindow")

        self.resize(QDesktopWidget().availableGeometry(self).size() * .7)

        self.uiFrame = QFrame(self)
        self.uiFrame.setFrameShape(QFrame.NoFrame)
        self.uiFrame.setFrameShadow(QFrame.Raised)
        self.uiFrame.setContentsMargins(0, 0, 0, 0)

        self.centralFrame = QFrame(self.uiFrame)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)

        self.spacerFrame = QFrame(self.centralFrame)
        self.spacerFrame.setFrameShape(QFrame.NoFrame)
        self.spacerFrame.setFrameShadow(QFrame.Raised)
        self.spacerFrame.setContentsMargins(0, 0, 0, 0)

        self.contentFrame = QFrame(self.centralFrame)
        self.contentFrame.setFrameShape(QFrame.NoFrame)
        self.contentFrame.setFrameShadow(QFrame.Raised)
        self.contentFrame.setContentsMargins(0, 0, 0, 0)

        self.homeFrame = QFrame(self.contentFrame)
        self.homeFrame.setFrameShape(QFrame.NoFrame)
        self.homeFrame.setFrameShadow(QFrame.Raised)
        self.homeFrame.setContentsMargins(0, 0, 0, 0)

        self.graphicsFrame = QFrame(self.homeFrame)
        self.graphicsFrame.setFrameShape(QFrame.NoFrame)
        self.graphicsFrame.setFrameShadow(QFrame.Raised)
        self.graphicsFrame.setContentsMargins(0, 0, 0, 0)

        # Assign Mask Graphics, Flow Graphics, and Flow Table Views To Right Graphics Panel
        self.rGraphicsFrame = QFrame(self.graphicsFrame)
        self.rGraphicsFrame.setFrameShape(QFrame.NoFrame)
        self.rGraphicsFrame.setFrameShadow(QFrame.Raised)
        self.rGraphicsFrame.setContentsMargins(0, 0, 0, 0)

        self.rGraphicsPanel = QTabWidget(self.rGraphicsFrame)
        self.rGraphicsPanel.addTab(self.maskGraphicsView, "Mask")
        self.rGraphicsPanel.addTab(self.flowGraphicsView, "Plot")
        self.rGraphicsPanel.addTab(self.flowTableView, "Analysis")
        self.rGraphicsPanel.setTabPosition(QTabWidget.North)
        self.rGraphicsPanel.setStyleSheet("QTabBar::tab { "
                                          "height: 30px; "
                                          "width: 100px; "
                                          "background-color: rgb(39, 44, 54);"
                                          "font: 14px;"
                                          "border-radius: 1px;"
                                          "}"
                                          "QTabBar::tab:selected { "
                                          "border: 1px solid gray;"
                                          "}"
                                          "QTabBar::tab:hover{"
                                          "background-color: rgb(85, 170, 255);"
                                          "}"
                                          "QTabWidget::pane {"
                                          "border: 1px solid gray;"
                                          "}")

        self.rGraphicsPanel.setCurrentIndex(1)
        self.rGraphicsPanel.setContentsMargins(0, 0, 0, 0)

        # Assign File Tree, Series Graphics, and Flow Graphics View to Left Graphics Panel
        self.lGraphicsFrame = QFrame(self.graphicsFrame)
        self.lGraphicsFrame.setFrameShape(QFrame.NoFrame)
        self.lGraphicsFrame.setFrameShadow(QFrame.Plain)
        self.lGraphicsFrame.setContentsMargins(0, 0, 0, 0)

        self.lGraphicsPanel = QTabWidget(self.lGraphicsFrame)
        self.lGraphicsPanel.addTab(self.fileTreeView, "File Browser")
        self.lGraphicsPanel.addTab(self.seriesGraphicsView, "Series")
        self.lGraphicsPanel.addTab(self.seriesTableView, "Meta Data")
        self.lGraphicsPanel.setTabPosition(QTabWidget.North)
        self.lGraphicsPanel.setStyleSheet("QTabBar::tab { "
                                          "height: 30px; "
                                          "width: 100px; "
                                          "background-color: rgb(39, 44, 54);"
                                          "font: 14px;"
                                          "border-radius: 1px;"
                                          "}"
                                          "QTabBar::tab:selected { "
                                          "border: 1px solid gray;"
                                          "}"
                                          "QTabBar::tab:hover{"
                                          "background-color: rgb(85, 170, 255);"
                                          "}"
                                          "QTabWidget::pane {"
                                          "border: 1px solid gray;"
                                          "}")

        self.lGraphicsPanel.setCurrentIndex(0)
        self.lGraphicsPanel.setContentsMargins(0, 0, 0, 0)

        # Create right graphics panel layout (mask/plot/analysisWidget on top, toolbar on bottom
        self.rGraphicsLayout = QVBoxLayout(self.rGraphicsFrame)
        self.rGraphicsLayout.addWidget(self.rGraphicsPanel)
        self.rGraphicsLayout.addWidget(self.toolBar)
        self.rGraphicsLayout.setContentsMargins(0, 0, 0, 0)

        # Create left graphics panel layout (mask/plot/analysisWidget on top, toolbar on bottom
        self.lGraphicsLayout = QVBoxLayout(self.lGraphicsFrame)
        self.lGraphicsLayout.addWidget(self.lGraphicsPanel)
        self.lGraphicsLayout.setContentsMargins(0, 0, 0, 0)
        self.lGraphicsLayout.setContentsMargins(0, 0, 0, 0)

        # Create horizontal layout (image/file system on left, mask/plot on right)
        self.graphicsLayout = QHBoxLayout(self.graphicsFrame)
        self.graphicsLayout.addWidget(self.lGraphicsFrame, stretch=1)
        self.graphicsLayout.addWidget(self.rGraphicsFrame, stretch=1)
        self.graphicsLayout.setContentsMargins(0, 0, 0, 0)

        # Create lower table layout (table on left, splash screen on right)
        self.tableFrame = QFrame(self.homeFrame)
        self.tableFrame.setContentsMargins(0, 0, 0, 0)

        self.tableLayout = QHBoxLayout(self.tableFrame)
        self.tableLayout.addWidget(self.patientTableView)
        self.tableLayout.setContentsMargins(0, 0, 0, 0)

        # Create vertical layout (graphics at top, table at bottom)
        self.homeLayout = QVBoxLayout(self.homeFrame)
        self.homeLayout.addWidget(self.graphicsFrame, stretch=3)
        self.homeLayout.addWidget(self.tableFrame, stretch=1)
        self.homeLayout.setContentsMargins(0, 0, 0, 0)

        self.contentLayout = QStackedLayout(self.contentFrame)
        self.contentLayout.addWidget(self.homeFrame)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setCurrentIndex(0)

        self.spacerLayout = QVBoxLayout(self.spacerFrame)
        self.spacerLayout.addWidget(self.contentFrame)
        self.spacerLayout.setContentsMargins(5, 5, 5, 5)

        self.centralLayout = QVBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.titleBar, alignment=Qt.AlignTop)
        self.centralLayout.addWidget(self.spacerFrame)
        self.centralLayout.addWidget(self.statusBar)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.centralLayout.setSpacing(0)

        self.uiLayout = QHBoxLayout(self.uiFrame)
        self.uiLayout.addWidget(self.sideMenu)
        self.uiLayout.addWidget(self.centralFrame)
        self.uiLayout.setSpacing(0)
        self.uiLayout.setContentsMargins(0, 0, 0, 0)

        self.setCentralWidget(self.uiFrame)
        self.centralWidget().setLayout(self.uiLayout)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.show()

    def moveWindow(self, ev):
        if ev.buttons() == Qt.LeftButton:
            self.move(self.pos() + ev.globalPos() - self.dragPos)
            self.dragPos = ev.globalPos()
            ev.accept()

    def mousePressEvent(self, ev):
        self.dragPos = ev.globalPos()
