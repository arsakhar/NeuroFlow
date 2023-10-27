from PyQt5.QtWidgets import QFileDialog
import pyqtgraph as pg
import csv
import os
from PIL import Image
import numpy as np

from .FlowToolbox import FlowToolbox
# from src.neuroflow import LabelGenerator


"""
Writes data associated with graphics and table widgets to output files
"""
class DataWriter():
    def __init__(self, flowTable, flowGraphics, seriesGraphics, maskGraphics, toolBar, fileSystem):
        self.toolBar = toolBar
        self.flowTable = flowTable
        self.flowGraphics = flowGraphics
        self.seriesGraphics = seriesGraphics
        self.maskGraphics = maskGraphics
        self.fileSystem = fileSystem

        self.saveDir = None
        self.filePrefix = None

        self.toolBar.saveBtn.clicked.connect(self.saveAll)
        self.toolBar.clearBtn.clicked.connect(lambda: self.toolBar.saveBtn.setDisabled(True))
        self.toolBar.clearBtn.clicked.connect(lambda: self.toolBar.saveTxtBox.setDisabled(True))

    """
    Called when a new ROI is created. Enables the save button option
    ================== ===========================================================================
    **Arguments:**
    imageROI           image roi ndarray
    ================== ===========================================================================
    """
    def newSegmentationBundle(self, segmentationBundle):
        self.toolBar.saveBtn.setDisabled(False)
        self.toolBar.saveTxtBox.setDisabled(False)

    """
    Saves flow plot and data, pixel intensity, velocity matrix, and viewbox for current image.
    Not practical to save pixel intensity, velocity matrix, and viewboxes for all images in series
    because that would take too much. However, this needs to be revisited and fleshed out better.
    """
    def saveAll(self):
        saveDialog = QFileDialog()
        saveDialog.setFileMode(QFileDialog.DirectoryOnly)
        location = saveDialog.getExistingDirectory(saveDialog,
                                             caption='Select Save Directory',
                                             directory=self.fileSystem.activeDir)

        self.saveDir = os.path.join(location, 'nf_output')

        if not os.path.exists(self.saveDir):
            os.makedirs(self.saveDir)

        self.filePrefix = self.toolBar.saveTxtBox.text()

        if self.filePrefix:
            self.filePrefix = self.filePrefix + "_"

        self.saveFlowTable(output_dir=self.saveDir, file_prefix=self.filePrefix)
        self.saveFlowGraphics(output_dir=self.saveDir, file_prefix=self.filePrefix, file_type='.png')
        self.saveSeriesGraphics(output_dir=self.saveDir, file_prefix=self.filePrefix, file_type='.png')
        # self.saveSeriesROI(output_dir=self.saveDir, file_prefix=self.filePrefix)
        # self.saveMaskGraphics(output_dir=self.saveDir, file_prefix=self.filePrefix, file_type='.png')
        # self.savePixelIntensityMatrix(output_dir=self.saveDir, file_prefix=self.filePrefix)
        # self.saveVelocityMatrix(output_dir=self.saveDir, file_prefix=self.filePrefix)

        # run this function if you want to create a labels file for semantic segmentation
        # self.saveSegmentationLabels(series=self.flowTable.series)

        self.toolBar.saveTxtBox.setDefaultText()

    """
    Saves the image path, mask path, subject id, and roi for semantic segmentation. This is probably
    not the best place to put this function but it works for now.
    For segmentation, mask mapping is as follows:
    1 - aqueduct (CA)
    2 - c2_c3 ss (SS)
    3 - internal jugular vein (IJV)
    4 - internal carotid artery (ICA)
    5 - vertebral artery (VA)
    This means that we will take the existing binary mask and change intensity based on the ROI
    we segmented. This allows for the model to differentiate between ROI's during training
    ================== ===========================================================================
    **Arguments:**
    series             the active series
    ================== ===========================================================================
    """
    def saveSegmentationLabels(self, series):
        roi = self.filePrefix[:-1]

        maskMapping = {'CA': 1, 'SS': 2, 'IJV': 3, 'ICA': 4, 'VA': 5}

        # exit if I don't save the ROI with the correct nomenclature
        if roi not in maskMapping:
            return

        segmentationType = maskMapping[roi]

        subject_id = os.path.basename(os.path.normpath(self.fileSystem.activeDir))
        filePrefix = subject_id + "_" + roi + "_"

        mask_dir = r'Z:\Ashwin\DataScience\Projects\FlowDyn\scripts\ML\labels\segmentation\masks'

        maskPath = self.saveMaskGraphics(output_dir=mask_dir,
                              file_prefix=filePrefix,
                              file_type='.png',
                              mask_intensity=segmentationType)

        maskPath = maskPath.replace('\\', '/')
        maskPath = maskPath.replace('Z:/', '/ifs/loni/faculty/jpa/')

        # labelGenerator = LabelGenerator()

        sequence = series.parentSequence

        # let's iterate through phase, complex difference, and magnitude images
        for series in sequence.series:
            type = series.getReconstructionType()

            # let's iterate through every image in the series
            for image in series.images:
                imgPath = os.path.join(self.fileSystem.activeDir, image.record.ReferencedFileID)
                imgPath = imgPath.replace('\\', '/')
                imgPath = imgPath.replace('Z:/', '/ifs/loni/faculty/jpa/')

                appendLine = [imgPath, subject_id, type, roi, maskPath]

                # labelGenerator.update_segmentation_labels_file(appendLine)

    """
    Saves pixel intensity values for phase roi ndarray
    NOTE: only saves values for current slice index. Rewrite function to save all slices
    (takes up a lot of storage (~ 1.8mb per 672x672 array)
    ================== ===========================================================================
    **Arguments:**
    output_dir         directory to save pixel intensity data csv
    file_prefix        file prefix
    ================== ===========================================================================
    """
    def savePixelIntensityMatrix(self, output_dir, file_prefix):
        flowToolbox = FlowToolbox()
        series = self.flowTable.series
        phaseSeries = series.parentSequence.getSeriesByType("Phase")

        # did we load the series containing the phase images?
        if phaseSeries is None:
            return

        phaseData = flowToolbox.imageROItoPhaseROI(imageROI=self.seriesGraphics.imageROI,
                                                   imageSeries=series,
                                                   phaseSeries=phaseSeries)

        np.savetxt(
            os.path.join(output_dir, file_prefix + 'pixel_intensity_matrix' + '.csv'),
            phaseData[self.seriesGraphics.currentIndex, :, :], delimiter=",")

    """
    Saves velocity values for phase roi ndarray
    NOTE: only saves values for current slice index. Rewrite function to save all slices
    (takes up a lot of storage (~ 1.8mb per 672x672 array)
    ================== ===========================================================================
    **Arguments:**
    output_dir         directory to save velocity data csv
    file_prefix        file prefix
    ================== ===========================================================================
    """
    def saveVelocityMatrix(self, output_dir, file_prefix):
        roiAnalysis = FlowToolbox()
        series = self.flowTable.series

        phaseSeries = series.parentSequence.getSeriesByType("Phase")

        # did we load the series containing the phase images?
        if phaseSeries is None:
            return

        phaseROI = roiAnalysis.imageROItoPhaseROI(imageROI=self.seriesGraphics.imageROI,
                                                  imageSeries=series,
                                                  phaseSeries=phaseSeries)

        velocityData = roiAnalysis.getVelocityMatrix(phaseROI, series.getVenc())
        np.savetxt(
            os.path.join(output_dir, file_prefix + 'velocity_matrix' + '.csv'),
            velocityData[self.seriesGraphics.currentIndex, :, :], delimiter=",")

    """
    Saves data from flow table
    ================== ===========================================================================
    **Arguments:**
    output_dir         directory to save flow data csv
    file_prefix        file prefix
    ================== ===========================================================================
    """
    def saveFlowTable(self, output_dir, file_prefix):
        path = os.path.join(output_dir, file_prefix
                            + 'flow_table'
                            + '.csv')

        if path:
            with open(str(path), 'w') as stream:
                writer = csv.writer(stream, lineterminator='\n')

                for row in range(self.flowTable.tableView.rowCount()):
                    rowdata = []

                    for column in range(self.flowTable.tableView.columnCount()):
                        item = self.flowTable.tableView.item(row, column)

                        if item is not None:
                            rowdata.append(item.text())
                        else:
                            rowdata.append('')

                    writer.writerow(rowdata)

    """
    Saves plot from flow graphics
    ================== ===========================================================================
    **Arguments:**
    output_dir         directory to save plot
    file_prefix        file prefix
    file_type          file type for saved plot (optional)
    ================== ===========================================================================
    """
    def saveFlowGraphics(self, output_dir, file_prefix, file_type=None):
        if file_type is None:
            file_type = '.png'

        path = os.path.join(output_dir, file_prefix + 'flow_plot' + file_type)

        exporter = pg.exporters.ImageExporter(self.flowGraphics.plotItem)

        exporter.export(path)

    """
    Saves only the roi from series graphics.
    NOTE: This option isn't very useful because the ROI can't be interpreted in a meaningful way 
    without the rest of the image.
    NOTE: Also only saving roi image current slice index. Rewrite function to save all slices (takes up space)
    ================== ===========================================================================
    **Arguments:**
    output_dir         directory to save plot
    file_prefix        file prefix
    file_type          file type for saved plot (optional)
    ================== ===========================================================================
    """
    def saveSeriesROI(self, output_dir, file_prefix, file_type=None):
        if file_type is None:
            file_type = '.png'

        roi = self.seriesGraphics.imageROI

        roi = np.nan_to_num(roi)

        currentIndex = self.seriesGraphics.currentIndex

        im_array = roi[currentIndex, :, :]
        im_array = (im_array - np.min(im_array))/np.ptp(im_array) * 255
        im_array = np.uint8(im_array)
        im = Image.fromarray(im_array, "L")

        path = os.path.join(output_dir, file_prefix + 'roi_image' + file_type)
        im.save(path)

    """
    Saves viewbox for current image in series graphics
    ================== ===========================================================================
    **Arguments:**
    output_dir         directory to save plot
    file_prefix        file prefix
    file_type          filetype for saved plot (optional)
    ================== ===========================================================================
    """
    def saveSeriesGraphics(self, output_dir, file_prefix, file_type=None):
        if file_type is None:
            file_type = '.png'

        path = os.path.join(output_dir, file_prefix + 'overlay_image' + file_type)

        exporter = pg.exporters.ImageExporter(self.seriesGraphics.view)

        exporter.export(path)

    """
    Saves the binary mask from mask graphics
    ================== ===========================================================================
    **Arguments:**
    output_dir         directory to save plot
    file_prefix        file prefix
    file_type          filetype for saved plot (optional)
    mask_intensity     the intensity of the binary mask. Can be any integer (optional)
    ================== ===========================================================================
    """
    def saveMaskGraphics(self, output_dir, file_prefix, file_type=None, mask_intensity=None):
        if file_type is None:
            file_type = '.png'

        mask = self.maskGraphics.maskItem.image

        mask = mask.T  # transpose mask back to row-major order (row, col)

        if mask_intensity:
            mask[mask == 1] = mask_intensity

        mask = (mask - np.min(mask))/np.ptp(mask) * 255
        mask = np.uint8(mask)
        mask = Image.fromarray(mask, "L")

        path = os.path.join(output_dir, file_prefix + 'mask_image' + file_type)

        if os.path.exists(path):
            path = os.path.join(output_dir, file_prefix + 'mask_image_2' + file_type)

        mask.save(path)

        return path
