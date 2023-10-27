from ..ToolBox.DataWriter import DataWriter


class UIController:
    def __init__(self, ui_main):
        super().__init__()

        self.ui_main = ui_main

        self.ui_titleBar = self.ui_main.titleBar
        self.ui_toolBar = self.ui_main.toolBar
        self.ui_sideMenu = self.ui_main.sideMenu
        self.ui_statusBar = self.ui_main.statusBar

        self.ui_fileTreeView = self.ui_main.fileTreeView
        self.ui_maskGraphicsView = self.ui_main.maskGraphicsView
        self.ui_flowGraphicsView = self.ui_main.flowGraphicsView
        self.ui_seriesGraphicsView = self.ui_main.seriesGraphicsView

        self.ui_patientTableView = self.ui_main.patientTableView
        self.ui_seriesTableView = self.ui_main.seriesTableView
        self.ui_flowTableView = self.ui_main.flowTableView

        self.ui_lGraphicsPanel = self.ui_main.lGraphicsPanel
        self.ui_contentLayout = self.ui_main.contentLayout

        self.overlay = self.ui_seriesGraphicsView.overlay
        self.autoSeg = self.ui_seriesGraphicsView.autoSeg

        self.dataWriter = DataWriter(self.ui_flowTableView,
                                     self.ui_flowGraphicsView,
                                     self.ui_seriesGraphicsView,
                                     self.ui_maskGraphicsView,
                                     self.ui_toolBar,
                                     self.ui_fileTreeView)

        self.setPatientLoadedCallbacks()
        self.setSeriesSelectedCallbacks()
        self.setNewROICallbacks()
        self.linkSeriesMaskViews()

        self.ui_fileTreeView.patientLoaded.connect(lambda: self.ui_lGraphicsPanel.setCurrentIndex(
            self.ui_main.SERIES_GRAPHICS_VIEW))

    def setPatientLoadedCallbacks(self):
        self.ui_fileTreeView.patientLoaded.connect(self.ui_patientTableView.newPatient)
        # self.ui_fileTreeView.patientLoaded.connect(self.ui_seriesGraphicsView.newPatient)
        # self.ui_fileTreeView.patientLoaded.connect(self.overlay.newPatient)
        # self.ui_fileTreeView.patientLoaded.connect(self.ui_maskGraphicsView.newPatient)
        # self.ui_fileTreeView.patientLoaded.connect(self.ui_flowGraphicsView.newPatient)
        # self.ui_fileTreeView.patientLoaded.connect(self.ui_seriesTableView.newPatient)
        # self.ui_fileTreeView.patientLoaded.connect(self.ui_flowTableView.newPatient)

    def setSeriesSelectedCallbacks(self):
        self.ui_patientTableView.seriesSelected.connect(self.ui_toolBar.seriesSelected)
        self.ui_patientTableView.seriesSelected.connect(self.ui_seriesGraphicsView.seriesSelected)
        self.ui_patientTableView.seriesSelected.connect(self.overlay.seriesSelected)
        self.ui_patientTableView.seriesSelected.connect(self.ui_maskGraphicsView.seriesSelected)
        self.ui_patientTableView.seriesSelected.connect(self.ui_flowGraphicsView.seriesSelected)
        self.ui_patientTableView.seriesSelected.connect(self.ui_seriesTableView.seriesSelected)
        self.ui_patientTableView.seriesSelected.connect(self.ui_flowTableView.seriesSelected)

    def linkSeriesMaskViews(self):
        self.ui_seriesGraphicsView.view.setXLink(self.ui_maskGraphicsView.view)
        self.ui_seriesGraphicsView.view.setYLink(self.ui_maskGraphicsView.view)
        self.overlay.newOverlay.connect(self.ui_maskGraphicsView.newOverlay)
        self.autoSeg.newAutoSeg.connect(self.ui_maskGraphicsView.newAutoSeg)
        self.ui_maskGraphicsView.newMask.connect(self.overlay.newMask)
        self.ui_maskGraphicsView.newMask.connect(self.ui_seriesGraphicsView.newMask)

    def setNewROICallbacks(self):
        self.ui_seriesGraphicsView.newSegmentationBundle.connect(self.ui_flowTableView.newSegmentationBundle)
        self.ui_seriesGraphicsView.newSegmentationBundle.connect(self.ui_flowGraphicsView.newSegmentationBundle)
        self.ui_seriesGraphicsView.newSegmentationBundle.connect(self.dataWriter.newSegmentationBundle)
