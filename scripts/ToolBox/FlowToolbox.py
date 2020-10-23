import numpy as np
import math

class FlowToolbox():
    def __init__(self):
        pass

    """
    Converts pixel intensity to velocity
    ================== ===========================================================================
    **Arguments:**
    ROIData            ROIData ndarray
    venc               venc value associated with image

    **Returns:**
    velocityData       list of velocity values
    ================== ===========================================================================
    """
    def getVelocityMatrix(self, ROIData, venc):
        maskedROI = np.ma.masked_invalid(ROIData)

        # we are assuming the image we get is a phase imageROI. phase range is 0 to 4095
        velocityROI = (maskedROI - (4095/2)) / ((4095/2) * math.pi) * venc

        return velocityROI

    """
    Converts pixel intensity to velocity
    ================== ===========================================================================
    **Arguments:**
    ROIData            ROIData ndarray
    venc               venc value associated with image

    **Returns:**
    velocityData       list of velocity values
    ================== ===========================================================================
    """
    def getVelocityData(self, ROIData, venc):
        maskedROI = np.ma.masked_invalid(ROIData)

        # we are assuming the image we get is a phase imageROI. phase range is 0 to 4095
        maskedROI = (maskedROI - (4095/2)) / ((4095/2) * math.pi) * venc

        velocityData = maskedROI.mean(axis=(1, 2))

        return velocityData

    """
    Calculates area of imageROI
    ================== ===========================================================================
    **Arguments:**
    ROIData            ROIData ndarray
    pixelArea          physical area of pixel
    
    **Returns:**
    roiArea            area of imageROI (mm^2)
    ================== ===========================================================================
    """
    def getArea(self, ROIData, pixelArea):
        nonNanPixels = np.count_nonzero(~np.isnan(ROIData[0, :, :]))
        roiArea = pixelArea * nonNanPixels

        roiArea = round(roiArea, 2)

        return roiArea

    """
    Calculates volume displaced of imageROI over 1 cardiac cycle
    ================== ===========================================================================
    **Arguments:**
    timeData           list of time values
    flowData           list of flow values
    
    **Returns:**
    volumeDisplaced    total displacement of fluid over cardiac cycle
    ================== ===========================================================================
    """
    def getVolumeDisplaced(self, timeData, flowData):
        if len(timeData) < 2:
            return None

        flowData = np.array(flowData)

        posFlow = np.copy(flowData)
        negFlow = np.copy(flowData)

        posFlow[posFlow < 0] = 0
        negFlow[negFlow > 0] = 0

        timeData = np.array(timeData)
        timeData = timeData / 1000  # convert ms to s

        posDisplacement = np.trapz(posFlow, timeData)
        negDisplacement = np.trapz(negFlow, timeData)

        volumeDisplaced = posDisplacement + abs(negDisplacement)

        volumeDisplaced = round(volumeDisplaced, 2)

        return volumeDisplaced

    """
    Calculates flow values for n-dimensional imageROI
    ================== ===========================================================================
    **Arguments:**
    velocityData       list of velocity values
    roiArea            area of imageROI

    **Returns:**
    flow               list of flow values (mm^3/s)
    ================== ===========================================================================
    """
    def getFlowData(self, velocityData, roiArea):
        flowData = velocityData * roiArea
        flowData = flowData.tolist()
        flowData = [round(flowPoint, 2) for flowPoint in flowData]

        return flowData

    """
    Calculates time values for n-dimensional imageROI
    ================== ===========================================================================
    **Arguments:**
    rrInterval         time for one heart beat
    numAcquisitions    number of acquisitions during one heart beat

    **Returns:**
    timeData           list of time values where length equals number of imageROI slices (ms)
    ================== ===========================================================================
    """
    def getTimeData(self, rrInterval, numAcquisitions):
        timeData = np.arange(0, rrInterval, rrInterval / numAcquisitions)

        timeData = timeData.tolist()

        timeData = [round(timePoint) for timePoint in timeData]

        return timeData

    """
    Calculates min flow
    ================== ===========================================================================
    **Arguments:**
    flowData           list of flow values

    **Returns:**
    minFlow            minimum flow
    ================== ===========================================================================
    """
    def getMinFlow(self, flowData):
        flowData = np.array(flowData)

        minFlow = np.min(flowData)

        return minFlow

    """
    Calculates max flow
    ================== ===========================================================================
    **Arguments:**
    flowData           list of flow values

    **Returns:**
    maxFlow            maximum flow
    ================== ===========================================================================
    """
    def getMaxFlow(self, flowData):
        flowData = np.array(flowData)

        maxFlow = np.max(flowData)

        return maxFlow

    """
    Calculates time to max flow
    ================== ===========================================================================
    **Arguments:**
    timeData           list of time values
    flowData           list of flow values

    **Returns:**
    timeToMaxFlow      time to max flow (ms)
    ================== ===========================================================================
    """
    def getTimeToMaxFlow(self, timeData, flowData):
        timeData = np.array(timeData)
        flowData = np.array(flowData)

        index = np.argmax(flowData)

        timeToMaxFlow = timeData[index]

        return timeToMaxFlow

    """
    Calculates time to min flow
    ================== ===========================================================================
    **Arguments:**
    timeData           list of time values
    flowData           list of flow values

    **Returns:**
    timeToMinFlow      time to min flow (ms)
    ================== ===========================================================================
    """
    def getTimeToMinFlow(self, timeData, flowData):
        timeData = np.array(timeData)
        flowData = np.array(flowData)

        index = np.argmin(flowData)

        timeToMinFlow = timeData[index]


        return timeToMinFlow

    """
    Calculates flow pulsatility
    ================== ===========================================================================
    **Arguments:**
    timeData           list of time values
    flowData           list of flow values

    **Returns:**
    pulsatility        slope of flow between min and max flow times (mm^3/s^2)
    ================== ===========================================================================
    """
    def getPulsatility(self, timeData, flowData):
        timeData = np.array(timeData)
        flowData = np.array(flowData)

        index = np.argmin(flowData)
        minFlow = flowData[index]
        timeAtMinFlow = timeData[index]

        index = np.argmax(flowData)
        maxFlow = flowData[index]
        timeAtMaxFlow = timeData[index]

        pulsatility = (maxFlow - minFlow) / (timeAtMaxFlow - timeAtMinFlow)

        pulsatility = abs(pulsatility)

        pulsatility = round(pulsatility, 2)

        return pulsatility

    """
    Calculates flow pulsatility index
    ================== ===========================================================================
    **Arguments:**
    flowData           list of flow values

    **Returns:**
    pulsatilityIndex   min and max flow difference divided by average flow
    ================== ===========================================================================
    """
    def getPulsatilityIndex(self, flowData):
        avgFlow = self.getAverageFlow(flowData)

        flowData = np.array(flowData)

        minFlow = np.min(flowData)
        maxFlow = np.max(flowData)

        pulsatilityIndex = (minFlow - maxFlow) / (avgFlow)

        pulsatilityIndex = abs(pulsatilityIndex)

        pulsatilityIndex = round(pulsatilityIndex, 2)

        return pulsatilityIndex

    """
    Calculates flow resistivity index
    ================== ===========================================================================
    **Arguments:**
    flowData           list of flow values

    **Returns:**
    resistivityIndex   min and max flow difference divided by specified flow
    ================== ===========================================================================
    """
    def getResistivityIndex(self, flowData, denominator):
        flowData = np.array(flowData)

        minFlow = np.min(flowData)
        maxFlow = np.max(flowData)

        if denominator == 'min':
            resistivityIndex = (minFlow - maxFlow) / (minFlow)

        else:
            resistivityIndex = (minFlow - maxFlow) / (maxFlow)

        resistivityIndex = abs(resistivityIndex)

        resistivityIndex = round(resistivityIndex, 2)

        return resistivityIndex

    """
    Calculates average flow
    ================== ===========================================================================
    **Arguments:**
    flowData           list of flow values

    **Returns:**
    avgFlow            average flow rate (mm^3/s)
    ================== ===========================================================================
    """
    def getAverageFlow(self, flowData):
        flowData = np.array(flowData)

        avgFlow = np.mean(flowData)

        avgFlow = round(avgFlow, 2)

        return avgFlow

    """
    Calculates flow pulse volume
    ================== ===========================================================================
    **Arguments:**
    timeData           list of time values
    flowData           list of flow values

    **Returns:**
    pulseVolume        volume under slope of flow between min and max flow times (mm^3)
    ================== ===========================================================================
    """
    def getPulseVolume(self, timeData, flowData):
        timeData = np.array(timeData)
        flowData = np.array(flowData)

        minIndex = np.argmin(flowData)

        maxIndex = np.argmax(flowData)

        timeData = timeData[minIndex:maxIndex + 1]
        flowData = flowData[minIndex:maxIndex + 1]

        pulseVolume = self.getVolumeDisplaced(timeData.tolist(), flowData.tolist())

        return pulseVolume

    """
    This method replaces the image imageROI with an equivalent phase imageROI. This is accomplished by 
    finding the series in the sequence that is of type 'phase'. We'll do some basic checks to ensure the 
    shape of the images and the pixel spacing matches. However, we have to assume that all flow series within 
    a sequence are acquired under the exact same conditions. Otherwise, this won't work.
    ================== ===========================================================================
    **Arguments:**
    imageROI           image roi ndarray
    imageSeries        active series
    phaseSeries        series within same sequence as active series that has phase information

    **Returns:**
    phaseROI           phase roi ndarray
    ================== ===========================================================================
    """
    def imageROItoPhaseROI(self, imageROI, imageSeries, phaseSeries):
        if phaseSeries is None:
            return

        images = []

        for image in phaseSeries.images:
            images.append(image.pixel_array)

        phaseROI = np.array(images)

        shapeMismatchFlag = (phaseROI.shape != imageROI.shape)
        pixelAreaMismatchFlag = (phaseSeries.images[0].getPixelArea() != imageSeries.images[0].getPixelArea())

        # do the series match in shape and pixel area? this is important for future analysisWidget
        if shapeMismatchFlag or pixelAreaMismatchFlag:
            return None

        imageROI = np.copy(imageROI)

        # set all non nan numbers to 1
        imageROI[~np.isnan(imageROI)] = 1

        # this is essentially an identity operation with the non roi region being set to nan
        phaseROI = phaseROI * imageROI

        return phaseROI
