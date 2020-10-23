import numpy as np

"""
Wrapper class for storing the Series information entity (IE) of the DICOM data model. Each Series IE can have or
more Image IE's. The Series IE consists of several modules and each modules contains one or more attributes.
http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.3.1

Record is a Directory Record of type 'SERIES' containing attributes from series modules
Series stores a reference to a list of associated Image IE's, defined by the Image wrapper class.

"""
class Series:
    def __init__(self):
        self.record = None
        self.images = []
        self.parentSequence = None

    """
    Calculates rrInterval
    ================== ===========================================================================
    **Returns:**
    rrInterval         time for 1 heart bate (s)
    ================== ===========================================================================
    """
    def getRRInterval(self):
        if len(self.images) < 2:
            return None

        triggerTimeAttr = 0x0018, 0x1060

        try:
            rrInterval = (self.images[1].dataset[triggerTimeAttr].value -
                          self.images[0].dataset[triggerTimeAttr].value) * len(self.images)

        except:
            rrInterval = None

        return rrInterval

    """
    Calculates beats per minute
    ================== ===========================================================================
    **Returns:**
    bpm                beats per minute
    ================== ===========================================================================
    """
    def getBPM(self):
        rrInterval = self.getRRInterval()

        if rrInterval is None:
            return None

        rrInterval = rrInterval * 10 ** -3

        bpm = str(round(60 / rrInterval))

        return bpm

    """
    Retrieves venc value for series if it exists
    ================== ===========================================================================
    **Returns:**
    venc               velocity encoding value
    ================== ===========================================================================
    """
    def getVenc(self):
        # let's try the private tag method first:
        vencAttr = 0x0051, 0x1014  # 0x0051, 0x1014 represents private tag data. venc value is defined here
        venc = None

        for image in self.images:
            try:
                venc = image.dataset[vencAttr].value
                venc = venc.split('_')[0]
                venc = venc[1:]
                venc = int(venc)
                venc = venc * 10  # convert venc from cm/s to mm/s

                break

            except:
                pass

        if venc is None:
            # 0x0008, 0x103e represents the series description. venc value can possibly be parsed from here
            seriesDescriptionAttr = 0x0008, 0x103e

            for image in self.images:
                try:
                    seriesDescription = image.dataset[seriesDescriptionAttr].value

                    start_index = seriesDescription.find("p2_") + 3
                    end_index = seriesDescription.find("venc_")

                    vencString = seriesDescription[start_index: end_index]

                    if vencString.isdigit():
                        venc = int(vencString)

                        venc = venc * 10  # convert venc from cm/s to mm/s

                        break

                except:
                    pass

        return venc

    """
    Retrieves series Type (magnitude, phase, difference). This is not formally defined in DICOM dictionary
    ================== ===========================================================================
    **Returns:**
    seriesType         the type of series
    ================== ===========================================================================
    """
    def getReconstructionType(self):
        imageTypeAttr = 0x0051, 0x1016  # 0x0051, 0x1016 represents reconstruction type
        seriesType = self.images[0].dataset[imageTypeAttr].value  # have to look at images to get type. using first.

        if "P" in seriesType:
            seriesType = "Phase"

        elif "MAG" in seriesType:
            seriesType = "Difference"

        elif "M" in seriesType:
            seriesType = "Magnitude"

        else:
            seriesType = None

        return seriesType

    """
    Retrieves series number
    ================== ===========================================================================
    **Returns:**
    seriesNumber       the series number
    ================== ===========================================================================
    """
    def getSeriesNumber(self):
        if self.record is None:
            seriesNumber = self.images[0].getSeriesNumber()  # check child image for series number if no record exists

        else:
            seriesNumber = self.record.SeriesNumber

        return seriesNumber