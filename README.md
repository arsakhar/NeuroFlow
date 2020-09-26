# NeuroFlow
## Cerebral Flow Dynamics - Brain Imaging Analysis Tool

![FitViz Banner](https://raw.githubusercontent.com/arsakhar/FitViz/master/readme/Logo.png?token=AJKJ6DYTD7J6XWH3QMPJTBS7LXHRO)

_Developed by Ashwin Sakhare_

NeuroFlow is a brain imaging tool designed for neuroscientists and clinicians to analyze cerebral flow dynamics from acquired MRI images. designed for neuroscientists and clinicians. It supports analysis of cerebral flow dynamics in the brain.

- - - -

### About ANT+

<a href="https://www.thisisant.com/" target="_blank">ANT+</a> is a wireless sensor network technology that allows you to moniter data broadcast from ANT+ capable devices. Fitness equipment, bike trainers, heart rate monitors, and blood pressure monitors are just a few of the many devices supported within the ANT+ ecosystem. Data broadcast from ANT+ devices is standardized based on the type of data being sent. ANT+ refers to a data type as a <a href="https://www.thisisant.com/developer/ant-plus/device-profiles" target="_blank">device profile</a>. An ANT+ device can broadcast data associated with multiple device profiles. For example, the Wahoo Kickr Snap broadcasts bicycle power and fitness equipment data.

- - - -

### Supported Devices
 
FitViz currently support the following device profiles:
* Heart Rate
* Bicycle Cadence
* Bicycle Speed
* Bicycle Speed & Cadence
* Bicycle Power
* Fitness Equipment

- - - -

### Installation

NeuroFlow was written in Python (v3.8.5). A distributable, NeuroFlow.exe, is included and can be executed as a standalone program. The distributable has only been tested on Windows 10 Pro (10.0.18363 Build 18363).
The source code isn't currently available for public use. However, I hope to make it public within the next few months.

- - - -

### User guide

Refer to the user manual located in the manual directory. 

- - - -

### About

The idea behind this project was to provide a standalone PC application for neuroscientists to use.

- - - -

### ToDo

- Improve speed of segmentation. The code needs to be optimized for speed.
- Add support for unstructured DICOM directories. The app currently only supports opening a DICOMDIR.
- Add support for creation of DICOMDIR from unstructured DICOM directories.
- Add threading so the app doesn't hang while processes are being executed.
- Perform a comprehensive QC check on the analysis pipeline. Need to make sure the results are accurate.
- Fix a bug related to converting an overlay to a binary mask and vice versa. 

- - - -

### Changelog

* v1.0.0 alpha (2020-09-26)
  * Initial release
  
- - - -

### Acknowledgements

NeuroFlow would not be possible without liberal imports of PyQt5, NumPy, Pandas, OpenCV, PyQtGraph, scikit-image, and Matplotlib. 
