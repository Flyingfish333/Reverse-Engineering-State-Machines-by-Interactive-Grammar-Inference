import sys
from PyQt5.QtWidgets import QApplication
from My_main_window import MyMainDialog

if __name__ == '__main__':
    # every last pyqt The program needs to have a QApplication object ,sys.argv Is a list of command line arguments
    app = QApplication(sys.argv) # Instantiation QApplication class , As GUI Main program entry
    ui = MyMainDialog() # example UI class

    ui.show() # Window display
    sys.exit(app.exec_()) # Enter the main loop of the program , In case of exit , To terminate the program