from FlowToolbox import FlowToolbox


"""
Class provides analysis of flow data. By convention, positive(+) flow values indicate flow is caudo-cranial 
(towards the head). Negative(-) flow values indicate flow in the cranio-caudal direction (away from the head). 
"""
class FlowPresets():
    AQUEDUCT = 'Aqueduct'
    C2_C3_SS = 'C2-C3 SS'
    ARTERY = 'Artery'
    VEIN = 'Vein'

    def __init__(self, activePreset):
        self.activePreset = activePreset

    def getDefaultMeasures(self, ROI, series):
        flowToolbox = FlowToolbox()

        roiArea = flowToolbox.getArea(ROI, series.images[0].getPixelArea())
        timeData = flowToolbox.getTimeData(series.getRRInterval(), len(series.images))
        velocityData = flowToolbox.getVelocityData(ROI, series.getVenc())
        flowData = flowToolbox.getFlowData(velocityData, roiArea)
        volumeDisplaced = flowToolbox.getVolumeDisplaced(timeData, flowData)
        minFlow = flowToolbox.getMinFlow(flowData)
        maxFlow = flowToolbox.getMaxFlow(flowData)

        singleMeasures = {
            'Preset': self.activePreset,
            'ROI Area (mm^2)': roiArea,
            'Minimum Flow (mm^3/s)': minFlow,
            'Maximum Flow (mm^3/s)': maxFlow,
            'Volume Displaced (mm^3)': volumeDisplaced
        }

        pairedMeasures = {
            'Time (ms) : Flow (mm^3/s)': [timeData, flowData]
        }

        return singleMeasures, pairedMeasures

    """
    Retreives all aqueductal measures
    ================== ===========================================================================
    **Arguments:**
    ROI                ROI ndarray
    series             the series object

    **Returns:**
    singleMeasures     measures with a single value per dictionary key
    pairedMeasures     measures with a list of values per dictionary key
    ================== ===========================================================================
    """
    def getAqueductMeasures(self, ROI, series):
        flowToolbox = FlowToolbox()

        roiArea = flowToolbox.getArea(ROI, series.images[0].getPixelArea())
        timeData = flowToolbox.getTimeData(series.getRRInterval(), len(series.images))
        velocityData = flowToolbox.getVelocityData(ROI, series.getVenc())
        flowData = flowToolbox.getFlowData(velocityData, roiArea)
        strokeVolume = flowToolbox.getVolumeDisplaced(timeData, flowData)
        flushPeak = flowToolbox.getMinFlow(flowData)
        fillPeak = flowToolbox.getMaxFlow(flowData)
        timeFlushPeak = flowToolbox.getTimeToMinFlow(timeData, flowData)
        timeFillPeak = flowToolbox.getTimeToMaxFlow(timeData, flowData)

        singleMeasures = {
            'Preset': self.activePreset,
            'ROI Area (mm^2)': roiArea,
            'Flush Peak (mm^3/s)': flushPeak,
            'Time Flush Peak (ms)': timeFlushPeak,
            'Fill Peak (mm^3/s)': fillPeak,
            'Time Fill Peak (ms)': timeFillPeak,
            'Stroke Volume (mm^3)': strokeVolume
        }

        pairedMeasures = {
            'Time (ms) : Flow (mm^3/s)': [timeData, flowData]
        }

        return singleMeasures, pairedMeasures

    """
    Retreives all c2-c3 measures. 
    ================== ===========================================================================
    **Arguments:**
    ROI                ROI ndarray
    series             the series object

    **Returns:**
    singleMeasures     measures with a single value per dictionary key
    pairedMeasures     measures with a list of values per dictionary key
    ================== ===========================================================================
    """
    def getC2C3Measures(self, ROI, series):
        flowToolbox = FlowToolbox()

        roiArea = flowToolbox.getArea(ROI, series.images[0].getPixelArea())
        timeData = flowToolbox.getTimeData(series.getRRInterval(), len(series.images))
        velocityData = flowToolbox.getVelocityData(ROI, series.getVenc())
        flowData = flowToolbox.getFlowData(velocityData, roiArea)
        strokeVolume = flowToolbox.getVolumeDisplaced(timeData, flowData)
        flushPeak = flowToolbox.getMinFlow(flowData)
        fillPeak = flowToolbox.getMaxFlow(flowData)
        timeFlushPeak = flowToolbox.getTimeToMinFlow(timeData, flowData)
        timeFillPeak = flowToolbox.getTimeToMaxFlow(timeData, flowData)

        singleMeasures = {
            'Preset': self.activePreset,
            'ROI Area (mm^2)': roiArea,
            'Flush Peak (mm^3/s)': flushPeak,
            'Time Flush Peak (ms)': timeFlushPeak,
            'Fill Peak (mm^3/s)': fillPeak,
            'Time Fill Peak (ms)': timeFillPeak,
            'Stroke Volume (mm^3)': strokeVolume
        }

        pairedMeasures = {
            'Time (ms) : Flow (mm^3/s)': [timeData, flowData]
        }

        return singleMeasures, pairedMeasures

    """
    Retreives all arterial measures. 
    ================== ===========================================================================
    **Arguments:**
    ROI                ROI ndarray
    series             the series object

    **Returns:**
    singleMeasures     measures with a single value per dictionary key
    pairedMeasures     measures with a list of values per dictionary key
    ================== ===========================================================================
    """
    def getArteryMeasures(self, ROI, series):
        flowToolbox = FlowToolbox()

        roiArea = flowToolbox.getArea(ROI, series.images[0].getPixelArea())
        timeData = flowToolbox.getTimeData(series.getRRInterval(), len(series.images))
        velocityData = flowToolbox.getVelocityData(ROI, series.getVenc())
        flowData = flowToolbox.getFlowData(velocityData, roiArea)
        strokeVolume = flowToolbox.getVolumeDisplaced(timeData, flowData)
        pulseVolume = flowToolbox.getPulseVolume(timeData, flowData)
        systolicPeakFlow = flowToolbox.getMaxFlow(flowData)
        timeSystolicPeak = flowToolbox.getTimeToMaxFlow(timeData, flowData)
        diastolicPeakFlow = flowToolbox.getMinFlow(flowData)
        timeDiastolicPeak = flowToolbox.getTimeToMinFlow(timeData, flowData)
        pulsatility = flowToolbox.getPulsatility(timeData, flowData)
        pulsatilityIndex = flowToolbox.getPulsatilityIndex(flowData)
        resistivityIndex = flowToolbox.getResistivityIndex(flowData, denominator='max')
        avgFlow = flowToolbox.getAverageFlow(flowData)

        singleMeasures = {
            'Preset': self.activePreset,
            'ROI Area (mm^2)': roiArea,
            'Systolic Peak Flow (mm^3/s)': systolicPeakFlow,
            'Time Systolic Peak (ms)': timeSystolicPeak,
            'Diastolic Peak Flow (mm^3/s)': diastolicPeakFlow,
            'Time Diastolic Peak (ms)': timeDiastolicPeak,
            'Stroke Volume (mm^3)': strokeVolume,
            'Pulse Volume (mm^3)': pulseVolume,
            'Pulsatility (mm^3/s^2)': pulsatility,
            'Pulsatility Index': pulsatilityIndex,
            'Resistivity Index': resistivityIndex,
            'Average Flow (mm^3/s)': avgFlow
        }

        pairedMeasures = {
            'Time (ms) : Flow (mm^3/s)': [timeData, flowData]
        }

        return singleMeasures, pairedMeasures

    """
    Retreives all venous measures. 
    ================== ===========================================================================
    **Arguments:**
    ROI                ROI ndarray
    series             the series object

    **Returns:**
    singleMeasures     measures with a single value per dictionary key
    pairedMeasures     measures with a list of values per dictionary key
    ================== ===========================================================================
    """
    def getVeinMeasures(self, ROI, series):
        flowToolbox = FlowToolbox()

        roiArea = flowToolbox.getArea(ROI, series.images[0].getPixelArea())
        timeData = flowToolbox.getTimeData(series.getRRInterval(), len(series.images))
        velocityData = flowToolbox.getVelocityData(ROI, series.getVenc())
        flowData = flowToolbox.getFlowData(velocityData, roiArea)
        strokeVolume = flowToolbox.getVolumeDisplaced(timeData, flowData)
        systolicPeakFlow = flowToolbox.getMinFlow(flowData)
        timeSystolicPeak = flowToolbox.getTimeToMinFlow(timeData, flowData)
        diastolicPeakFlow = flowToolbox.getMaxFlow(flowData)
        timeDiastolicPeak = flowToolbox.getTimeToMaxFlow(timeData, flowData)
        avgFlow = flowToolbox.getAverageFlow(flowData)

        singleMeasures = {
            'Preset': self.activePreset,
            'ROI Area (mm^2)': roiArea,
            'Systolic Peak Flow (mm^3/s)': systolicPeakFlow,
            'Time Systolic Peak (ms)': timeSystolicPeak,
            'Diastolic Peak Flow (mm^3/s)': diastolicPeakFlow,
            'Time Diastolic Peak (ms)': timeDiastolicPeak,
            'Stroke Volume (mm^3)': strokeVolume,
            'Average Flow (mm^3/s)': avgFlow
        }

        pairedMeasures = {
            'Time (ms) : Flow (mm^3/s)': [timeData, flowData]
        }

        return singleMeasures, pairedMeasures
