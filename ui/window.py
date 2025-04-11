from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import QtGui
from ui import dashboard, budgets, reports, settings
from ui.transactions import transaction
import ctypes

class MainWindow(QWidget):


    def __init__(self):
        super().__init__()
        self.tabs = None
        self.icon = None
        self.mode = "Light"
        self.init_ui()

    def init_ui(self):
        # Create layout
        icon = QtGui.QIcon("resources/ico/icon.ico")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create QTabWidget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Add tabs

        dashboardTab = dashboard.DashboardWidget()
        transactionTab = transaction.TransactionWidget()
        budgetsTab = budgets.BudgetsWidget()
        reportsTab = reports.ReportsWidget()
        settingsTab = settings.SettingsWidget()

        self.tabs.addTab(dashboardTab, "Dashboard")
        self.tabs.addTab(transactionTab, "Transactions")
        self.tabs.addTab(budgetsTab, "Budgets")
        self.tabs.addTab(reportsTab, "Reports")
        self.tabs.addTab(settingsTab, "Settings")


        # Set window properties
        self.setWindowIcon(icon)
        self.setWindowTitle("Spendwise")
        self.setGeometry(500, 500, 737, 450)
        self.setMinimumSize(737,450)
        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.show()

        settingsTab.state_changed.connect(dashboardTab.modeChange)
        settingsTab.state_changed.connect(transactionTab.modeChange)
        settingsTab.state_changed.connect(budgetsTab.modeChange)
        settingsTab.state_changed.connect(reportsTab.modeChange)
        settingsTab.state_changed.connect(self.modeChange)

        with open('ui/stylesheets/light/mainstyle.css', 'r') as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)


    def modeChange(self, state):
        if state:
            with open('ui/stylesheets/dark/mainstyleDark.css', 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
                self.mode = "Dark"
        else:
            with open('ui/stylesheets/light/mainstyle.css', 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
                self.mode = "Light"


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.mode=="Dark":
            painter.fillRect(self.rect(), QColor("black"))
        else:
            painter.fillRect(self.rect(), QColor("white"))