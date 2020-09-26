# ![NeuroFlow Banner](https://raw.githubusercontent.com/arsakhar/NeuroFlow/master/readme/Logo.png) NeuroFlow
### Brain Imaging Tool for Analyzing Cerebral Flow Dynamics

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

### Quick Start

#### Load Patient Data

![File Browser Tab](https://raw.githubusercontent.com/arsakhar/NeuroFlow/master/readme/FileBrowser.png)

* Select the File Browser tab. Select the DICOMDIR file associated with the patient to be analyzed. Double click the highlighted selection to load the patient.

#### Segment ROI

* Select the Series tab.
* Select a pen from the color palette of pens in the toolbar.

![Toolbar](https://raw.githubusercontent.com/arsakhar/NeuroFlow/master/readme/Pen.png)

* Click inside the left view panel and drag the left mouse draw a contour around the desired ROI.

![Series Tab](https://raw.githubusercontent.com/arsakhar/NeuroFlow/master/readme/Segmentation.png)

* To make fine adjustments to the segmentation, select the Mask tab.
* Select a stamp from the slider in the toolbar.

![Toolbar](https://raw.githubusercontent.com/arsakhar/NeuroFlow/master/readme/Stamp.png)

* Select the Mask tab.
* Click inside the right view panel over to add/remove a mask at a single square pixel or click and drag to modify multiple pixels.

![Mask Tab](https://raw.githubusercontent.com/arsakhar/NeuroFlow/master/readme/Mask.png)

#### View Plot

* Select the Plot tab.
* Plots for each segmentation can be viewed here.

![Plot Tab](https://raw.githubusercontent.com/arsakhar/NeuroFlow/master/readme/Plot.png)

#### View Analysis

* Select the Analysis tab.
* A table of flow measurements for each segmentation can be viewed here.

![Analysis Tab](https://raw.githubusercontent.com/arsakhar/NeuroFlow/master/readme/Analysis.png)

#### Save Analysis

* Enter an ROI name in the input box on the toolbar.
* Select the save icon, specify a save directory, and select ok.
* Plots, tables, and images are saved to the specified directory.

![Toolbar](https://raw.githubusercontent.com/arsakhar/NeuroFlow/master/readme/Save.png)

- - - -

### About

The idea behind this project was to provide an quick and easy tool for neuroscientists and clinicians to assess cerebral flow dynamics in the brain. To my knowledge, BioFlow is the only publicly available flow analysis software.<sup>1</sup>

1. Balédent O, Henry‐Feugeas MC, Idy‐Peretti I. Cerebrospinal fluid dynamics and relation with blood flow: a magnetic resonance study with semiautomated cerebrospinal fluid segmentation. Invest Radiol. 2001;36:368–377.

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

- - - -

### Disclaimer

NeuroFlow has not been rigorously QC tested and we claim no responsibility for inacurrate results.

