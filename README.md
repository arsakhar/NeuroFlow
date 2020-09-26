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

### Quick Start

There are 3 primary tabs on the client GUI: Networking, View, and Logging.

#### Networking

![Networking Tab](https://raw.githubusercontent.com/arsakhar/FitViz/master/readme/Networking.PNG?token=AJKJ6DYYPYFCCU5FLMTS7GC7LXHQI)

The _Networking_ tab is used to connect to ANT+ devices. 

* Select _Run_ under _Network Controls_ to scan for ANT+ devices. ANT+ devices identified during the scan period (5 seconds) are displayed under _Broadcasting Devices_. If ANT+ devices are identified, the network driver continues to listen indefinitely for incoming ANT+ messages.
* If a device is unknown, it will be named "Unknown Device <device number>". You can double click on the device entry under _Broadcasting Devices_ to rename the device. The name change will not take effect until the ANT+ session is restarted.
* Once an ANT+ session is started, it will continue to run indefinitely. An ANT+ session can be closed by selecting _Stop_ under Network Controls.
* _Reset_ can be used to reset measurement values that accumulate over time. For example, some ANT+ messages associated with a Bicycle Trainer included distance traveled and elapsed time, which are accumulated measurements. _Reset_ will set those measurement values to 0.
* _Network Statistics_ displays basic ANT+ network statistics including: # messages received, # ANT+ devices broadcasting, # device profiles received, and message frequency.

#### View

![View Tab](https://raw.githubusercontent.com/arsakhar/FitViz/master/readme/View.PNG?token=AJKJ6D6PGS322O5LQQGOGUC7LXHO4)

The _View_ tab is used to visualize measurement data from ANT+ devices. There are 4 viewing panels allowing for up to 4 measurements to be viewed concurrently in real-time.

* Select a device from the _Devices_ dropdown box.
* Select a profile from the _Profiles_ box.
* Select a data page from the _Data Pages_ box.
* Select a page measurement from the _Page Measurements_ box.

The measurement will be displayed via a gauge or LCD number depending on the type of measurement. Generally speaking, accumulated measurements will be displayed as an LCD number while measurements that fall within a range will be displayed via the gauge.

#### Logging

![Logging Tab](https://raw.githubusercontent.com/arsakhar/FitViz/master/readme/CSV.PNG?token=AJKJ6D6EH7ITDXT4DTPURUC7LXHNO)

The _Logging_ tab is used to log measurement data.

There are 2 logging options: UDP and CSV. CSV logging is simply writing data to a user-specified CSV file. For UDP logging, data is written to the user-specified ip address and port. The intent behind UDP is to allow for real-time data transfer to another program or device. In both cases, data is written each time a message is received.

* First, begin by adding the measurements you would like to track.
* For CSV logging, set the filename and select _Start_ to begin logging.
* For UDP logging, set the _Port_ and _IP Address_ select _Start_ to begin logging.
* UDP data is delivered as a byte array of the following format: [measurement 1 value; measurement 2 value; measurement 3 value; measurement 4 value; ...]

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
