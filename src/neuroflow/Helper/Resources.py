from PyQt5.QtCore import QSettings
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS,
        # so resources are bundled with the executable
        base_path = sys._MEIPASS
    else:
        # In development, resource files are in the same directory as the script
        base_path = os.path.abspath("./neuroflow")

    return os.path.join(base_path, relative_path)

appSettings = QSettings("Brain Tools", "NeuroFlow")
