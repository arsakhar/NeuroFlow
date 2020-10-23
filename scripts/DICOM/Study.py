"""
Wrapper class for storing the Study information entity (IE) of the DICOM data model. Each Study IE can have or
more Series IE's. The Study IE consists of several modules and each modules contains one or more attributes.
http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.4

Record is a Directory Record of type 'STUDY' containing attributes from study modules
Series stores a reference to a list of associated Series IE's, defined by the Series wrapper class.

"""
class Study:
    def __init__(self):
        self.record = None
        self.series = []

    """
    Retrieves study id
    ================== ===========================================================================
    **Returns:**
    studyID            the study ID
    ================== ===========================================================================
    """
    def getStudyID(self):
        if self.record is None:
            studyID = self.series[0].images[0].getStudyID()  # check child image for study ID

        else:
            studyID = self.record.StudyID

        return studyID