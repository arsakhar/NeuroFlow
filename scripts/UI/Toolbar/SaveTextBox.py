from PyQt5.QtWidgets import QLineEdit


"""
Widget to create save text box
"""
class SaveTextBox(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)

        self.defaultText = "Enter name of roi..."
        self.initUI()

    def initUI(self):
        self.setStyleSheet("border: 1px solid gray;")

        self.setDefaultText()
        self.setDisabled(True)

    def setDefaultText(self):
        self.clear()
        self.setPlaceholderText(self.defaultText)
