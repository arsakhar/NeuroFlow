"""
Stores a list of all series that are associated with the same sequence
"""
class Sequence:
    def __init__(self, refSeries, study):
        self.series = []
        self.name = None

        self.setSequence(refSeries, study)

    """
    Finds and all series associated with same sequence as the provided series. We will use the 
    protocol name attribute as the identifier due to subtle differences in the sequence names attribute.
    Is there a better attribute to look at?
    ================== ===========================================================================
    **Arguments:**
    series             reference series
    study              study
    ================== ===========================================================================
    """
    def setSequence(self, refSeries, study):
        self.name = refSeries.images[0].getProtocolName()

        for series in study.series:
            sequenceName = series.images[0].getProtocolName()

            # check if the sequence name for the reference series matches the
            # sequence name for the current series in the loop
            if self.name == sequenceName:
                self.series.append(series)

    """
    Finds and returns series of a given type. Options are "Phase", "Magnitude", "Difference"
    ================== ===========================================================================
    **Returns:**
    series             series of provided type
    ================== ===========================================================================
    """
    def getSeriesByType(self, type):
        for series in self.series:
            seriesType = series.getReconstructionType()

            # check if series is a phase type
            if seriesType == type:
                return series

        return None