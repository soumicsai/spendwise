from ui import window
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    window = window.MainWindow()
    app.exec_()

