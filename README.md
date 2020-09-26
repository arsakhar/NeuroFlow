# NeuroFlow
## Brain Imaging Tool - Analyzing Cerebral Flow Dynamics

![NeuroFlow Banner](https://raw.githubusercontent.com/arsakhar/FitViz/master/readme/Logo.png?token=AJKJ6DYTD7J6XWH3QMPJTBS7LXHRO)

_Developed by Ashwin Sakhare_

NeuroFlow is an imaging tool that allows neuroscientists and clinicians to analyze cerebral flow dynamics in the brain. The continuous circulation of cerebrospinal fluid (CSF) and cerebral blood flow (CBF) is key to the health of our central nervous system. When CSF and CBF dynamics in the brain become dysregulated, pathophysiological
states can occur. As such, cerebral flow dynamics may be an important biomarker for identifying meaningful alterations in neurological diseases.

Phase-contrast MRI (PC-MRI) is a validated, non-invasive MRI imaging technique, allowing rapid measurements of CSF and CBF flow in the brain. NeuroFlow provides a user-friendly interface for neuroscientists and clinicians to analyze PC-MRI images and extract measurements associated with cerebral flow dynamics. Moreover, NeuroFlow provides numerous tools to help user's quickly, accurately, and painlessly analyze flow data.

- - - -

### Installation

NeuroFlow was written in Python (v3.8.5). A distributable, NeuroFlow.exe, is included and can be executed as a standalone program. The distributable has only been tested on Windows 10 Pro (10.0.18363 Build 18363).

The source code isn't currently available for public use. However, I hope to make it public within the next few months.

- - - -

### User guide

Refer to the user manual located in the manual directory for a comprehensive guide on using NeuroFlow.

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
