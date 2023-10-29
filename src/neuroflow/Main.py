import sys

from .UI.Application import Application
from .UI.MainWindow import MainWindow
from .UIControllers.UIController import UIController


def run():
    """
    Main function to run the NeuroFlow application.
    """
    try:
        app = Application(sys)
        ui_main = MainWindow()
        ui_controller = UIController(ui_main)
        sys.exit(app.exec_())

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    run()
