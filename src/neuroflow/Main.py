from UI.MainWindow import MainWindow
from UI.Application import Application
from UIControllers.UIController import UIController

import sys


class FlowDyn:
    def __init__(self):
        pass

    def run(self):
        self.app = Application(sys)
        self.ui_main = MainWindow()

        self.ui_controller = UIController(self.ui_main)

        sys.exit(self.app.exec_())


"""
Entry point for entire application
"""
if __name__ == '__main__':
    FlowDyn().run()