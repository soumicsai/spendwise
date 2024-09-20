from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout)
from ui.PyToggle import PyToggle


class SettingsWidget(QWidget):
    state_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        layouth = QHBoxLayout()
        self.toggle_button = PyToggle()
        self.label = QLabel(self)
        self.label.setText("Light Mode")
        layouth.addWidget(self.label)
        layouth.addWidget(self.toggle_button)
        self.setLayout(layouth)
        self.toggle_button.stateChanged.connect(self.toggled)
        self.toggle_button.stateChanged.connect(self.repaint)

    def toggled(self):
        self.state_changed.emit(self.toggle_button.isChecked())
        if self.toggle_button.isChecked():
            self.label.setText("Dark Mode")
            with open('ui/stylesheets/dark/settingsDark.css', 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        else:
            self.label.setText("Light Mode")
            with open('ui/stylesheets/light/settingsLight.css', 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.toggle_button.isChecked():
            painter.fillRect(self.rect(), QColor("black"))
        else:
            painter.fillRect(self.rect(), QColor("white"))
