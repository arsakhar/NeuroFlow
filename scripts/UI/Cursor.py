from PyQt5.QtCore import Qt
from PyQt5 import QtGui


"""
Custom cursor class
"""
class Cursor(QtGui.QCursor):
    def __init__(self):
        super().__init__()

        self.DefaultCursor = Qt.ArrowCursor
        self.CrossCursor = Qt.CrossCursor
        self.ClosedHandCursor = Qt.ClosedHandCursor
