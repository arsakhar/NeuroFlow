from src.neuroflow.DICOM.Patient import Patient
from src.neuroflow.DICOM.Study import Study
from src.neuroflow.DICOM.Series import Series
from src.neuroflow.DICOM.Image import Image

import pydicom as dicom
from pydicom.filereader import read_dicomdir
import os
from _collections import defaultdict


"""
Read in DICOMDir file using pydicom
https://pydicom.github.io/pydicom/dev/auto_examples/input_output/plot_read_dicom_directory.html
"""
class DICOMReader:
    def __init__(self):
        pass

    """
    Steps down DICOMDir hierarchy and saves each information entity (IE) into it's respective class:
        -> patient
            -> study
                -> series
                    -> images

    ================== ===========================================================================
    **Arguments:**
    dicomdir_path      file path of DICOMDir file

    **Returns:**
    patient            instance of Patient
    ================== ===========================================================================
    """
    def load_patient_record(self, dicomdir_path):
        dicomdir = read_dicomdir(dicomdir_path)

        # we can't handle more than one patient at the moment
        if len(dicomdir.patient_records) > 1:
            return None

        # iterate over patient records for a patient
        for patient_record in dicomdir.patient_records:
            patient = Patient()
            patient.record = patient_record

            studies = patient_record.children

            # iterate over study records for a patient record
            for study_record in studies:
                study = Study()
                study.record = study_record
                patient.studies.append(study)

                _series = study_record.children

                # iterate over series records for a study record
                for series_record in _series:
                    series = Series()

                    series.record = series_record
                    study.series.append(series)

                    images = series_record.children

                    # iterate over image records for a series record
                    for image_record in images:
                        image = Image()
                        image.record = image_record

                        patient_dir = os.path.dirname(dicomdir_path)
                        image_path = os.path.join(patient_dir, image.record.ReferencedFileID)
                        image.dataset = dicom.dcmread(image_path)
                        image.pixel_array = image.dataset.pixel_array

                        series.images.append(image)

        return patient

    def load_dicom(self, dicom_path):
        image = dicom.dcmread(dicom_path)

        return image

    def try_parse_dir(self, dir_path):
        images = []

        for root, dirs, files in os.walk(dir_path, topdown=True):
            for file in files:
                if ("IMA" not in file) and ("dcm" not in file):
                    continue

                dcmPath = os.path.join(root, file)

                try:
                    image = Image()
                    image.dataset = dicom.dcmread(dcmPath)

                    image.pixel_array = image.dataset.pixel_array

                    images.append(image)

                except:
                    print('not a DICOM file!')


        # let's first group all images into their respective series
        # create a dictionary that pairs the image with it's series number
        imageSeriesPair = {}

        for image in images:
            seriesNumber = image.getSeriesNumber()
            imageSeriesPair.update({image: seriesNumber})

        # group images by same series number
        groupedImages = defaultdict(list)

        for image, seriesNumber in sorted(imageSeriesPair.items(), key=lambda x: x[1], reverse=False):
            groupedImages[seriesNumber].append(image)

        _series = []
        for key, val in groupedImages.items():
            series = Series()

            series.images = groupedImages[key]

            _series.append(series)

        # now let's group all series into their respective study
        # create a dictionary that pairs the image with it's study ID
        seriesStudyPair = {}

        for series in _series:
            studyID = series.images[0].getStudyID()  # pick first image from series
            seriesStudyPair.update({series: studyID})

        # group series by same study ID
        groupedSeries = defaultdict(list)

        for image, studyID in sorted(seriesStudyPair.items(), key=lambda x: x[1], reverse=False):
            groupedSeries[studyID].append(image)

        studies = []
        for key, val in groupedSeries.items():
            study = Study()

            study.series = groupedSeries[key]

            studies.append(study)

        # finally let's group all studies into their respective patient
        # create a dictionary that pairs the image with it's study ID
        studyPatientPair = {}

        for study in studies:
            studyID = study.series[0].images[0].getStudyID()  # pick first image from series
            studyPatientPair.update({study: studyID})

        # group studies by same patient ID
        groupedStudy = defaultdict(list)

        for image, studyID in sorted(studyPatientPair.items(), key=lambda x: x[1], reverse=False):
            groupedStudy[studyID].append(image)

        patient = None

        # we are only saving the first patient because we can't handle multiple patients at the moment
        for key, val in groupedStudy.items():
            patient = Patient()

            patient.studies = groupedStudy[key]

            break

        return patient