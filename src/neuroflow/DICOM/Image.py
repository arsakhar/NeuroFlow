"""
Wrapper class for storing the Image information entity (IE) of the DICOM data model.
The Image IE consists of several modules and each modules contains one or more attributes.
http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.7.6.1

Record is a Directory Record of type 'IMAGE' containing attributes from image modules (general image, mr image)
DataSet contains data and sequence information associated with the image
Pixel Array contains the pixel data associated with the image

"""
class Image:
    def __init__(self):
        self.record = None
        self.dataset = None
        self.pixel_array = None

    """
    Retrieves pixel area of image
    ================== ===========================================================================
    **Returns:**
    pixelArea          the area (mm^2) of a pixel
    ================== ===========================================================================
    """
    def getPixelArea(self):
        pixelAttr = 0x0028, 0x0030  # 0x0028, 0x0030 represents pixel spacing
        pixelArea = self.dataset[pixelAttr].value
        pixelArea = pixelArea[0] * pixelArea[1]

        return pixelArea

    """
    Retrieves protocol name associated with image
    ================== ===========================================================================
    **Returns:**
    protocolName       the name of the protocol
    ================== ===========================================================================
    """
    def getProtocolName(self):
        protocolNameAttr = 0x0018, 0x1030  # 0x0018, 0x1030 represents the protocol name
        protocolName = self.dataset[protocolNameAttr].value

        return protocolName

    """
    Retrieves acquisition time associated with image
    ================== ===========================================================================
    **Returns:**
    acquisitionTime    time of image acquisition
    ================== ===========================================================================
    """
    def getAcquisitionTime(self):
        acquisitionTimeAttr = 0x0008, 0x0032  # 0x0008, 0x0032 represents the acquisition time
        acquisitionTime = self.dataset[acquisitionTimeAttr].value

        return acquisitionTime

    """
    Retrieves series number
    ================== ===========================================================================
    **Returns:**
    seriesNumber       the series number
    ================== ===========================================================================
    """
    def getSeriesNumber(self):
        seriesAttr = 0x0020, 0x0011 # 0x0020, 0x0011 represents the series number
        seriesNumber = self.dataset[seriesAttr].value

        return seriesNumber

    """
    Retrieves patient id
    ================== ===========================================================================
    **Returns:**
    patientID          the patient ID
    ================== ===========================================================================
    """
    def getPatientID(self):
        patientAttr = 0x0010, 0x0020  # 0x0010, 0x0020 represents patient ID
        patientID = self.dataset[patientAttr].value

        return patientID

    """
    Retrieves study id
    ================== ===========================================================================
    **Returns:**
    studyID            the study ID
    ================== ===========================================================================
    """
    def getStudyID(self):
        studyAttr = 0x0020, 0x0010  # 0x0020, 0x0010 represents study ID
        studyID = self.dataset[studyAttr].value

        return studyID
