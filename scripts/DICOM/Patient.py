"""
Wrapper class for storing the Patient information entity (IE) of the DICOM data model. Each Patient IE can have or
more Study IE's. The Patient IE consists of several modules and each modules contains one or more attributes.
http://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_C.2

Record is a Directory Record of type 'PATIENT' containing attributes from patient modules
Studies stores a reference to a list of associated Study IE's, defined by the Study wrapper class.

"""
class Patient:
    def __init__(self):
        self.record = None
        self.studies = []

    """
    Retrieves patient id
    ================== ===========================================================================
    **Returns:**
    patientID          the patient ID
    ================== ===========================================================================
    """
    def getPatientID(self):
        if self.record is None:
            patientID = self.studies[0].series[0].images[0].getPatientID()  # check child image for patient ID

        else:
            patientID = self.record.PatientID

        return patientID