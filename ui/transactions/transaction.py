from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QScrollArea,
                             QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QSizePolicy,
                             QComboBox)
from PyQt5 import QtGui
from db import transactiondb
from ui.transactions.transactionWindow import TransactionWindow


class ComboBoxWithoutArrow(QComboBox):
    def __init__(self, parent=None):
        super(ComboBoxWithoutArrow, self).__init__(parent)

        # Remove the dropdown arrow
        self.setStyleSheet("QComboBox::drop-down { border: 0; }")

        # Add items to the combobox
        self.addItem("All")
        self.addItem("Today")
        self.addItem("Last 7 Days")
        self.addItem("Last 30 Days")


class TransactionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.filterButton = None
        self.trans_window = None
        self.transaction_list = QTableWidget()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        search_bar = QLineEdit()
        addTransaction = QPushButton("+")
        addTransaction.clicked.connect(self.transaction_window)
        search_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.transaction_list.setColumnCount(4)
        self.transaction_list.setHorizontalHeaderLabels(["Name", "Category", "Amount", "Date"])
        self.transaction_list.setSelectionBehavior(QTableWidget.SelectRows)
        transactions = transactiondb.show_transactions()
        sort_combo = QComboBox()
        sort_combo.addItem("Newest to Oldest")
        sort_combo.addItem("Oldest to Newest")
        sort_combo.addItem("Name")
        sort_combo.addItem("Amount")

        if transactions:
            for i in transactions:
                self.multi_column_list_item(i)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.transaction_list)
        search_bar.setPlaceholderText("Search transactions...")
        self.filterButton = ComboBoxWithoutArrow()
        self.filterButton.currentIndexChanged.connect(self.onCurrentIndexChanged)
        search_bar.textChanged.connect(self.search_text_changed)
        tab2_layout1 = QHBoxLayout()
        tab2_layout2 = QVBoxLayout()
        tab2_layout1.addWidget(search_bar)
        tab2_layout1.addWidget(self.filterButton)
        tab2_layout1.addWidget(sort_combo)
        tab2_layout1.addWidget(addTransaction)
        tab2_layout2.addWidget(scroll_area)
        main_layout.addLayout(tab2_layout1)
        main_layout.addLayout(tab2_layout2)
        with open('ui/stylesheets/light/transactions.css', 'r') as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

    def onCurrentIndexChanged(self):
        records = transactiondb.filter_transactions(self.filterButton.currentText())
        if records:
            self.transaction_list.clear()
            self.transaction_list.setHorizontalHeaderLabels(["Name","Category", "Amount", "Date"])
            self.transaction_list.setRowCount(0)
            for i in records:
                self.multi_column_list_item(i)
        else:
            self.transaction_list.clear()
            self.transaction_list.setHorizontalHeaderLabels(["Name","Category", "Amount", "Date"])
            self.transaction_list.setRowCount(0)

    def reinsert(self, records):
        if records:
            self.transaction_list.clear()
            self.transaction_list.setHorizontalHeaderLabels(["Name","Category", "Amount", "Date"])
            self.transaction_list.setRowCount(0)
            for i in records:
                self.multi_column_list_item(i)
        else:
            self.transaction_list.setRowCount(0)
            #transactions = transactiondb.show_transactions()
            #if transactions:
                #for i in transactions:
                    #self.multi_column_list_item(i)

    def search_text_changed(self, text):
        records = transactiondb.search_results(text)
        self.reinsert(records)

    def multi_column_list_item(self, data):
        current_row_count = self.transaction_list.rowCount()
        self.transaction_list.insertRow(current_row_count)
        col = 0
        for i in data:
            self.transaction_list.setItem(current_row_count, col, QTableWidgetItem(str(i)))
            col += 1

    def transaction_window(self):
        icon = QtGui.QIcon("resources/ico/icon.ico")
        self.trans_window = TransactionWindow()
        self.trans_window.setWindowIcon(icon)
        self.trans_window.setGeometry(500, 500, 544, 400)
        self.trans_window.show()
        self.trans_window.content_changed.connect(self.multi_column_list_item)

    def modeChange(self, state):
        if state:
            with open('ui/stylesheets/dark/transactionsDark.css', 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
                self.mode = "Dark"
        else:
            with open('ui/stylesheets/light/transactions.css', 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
                self.mode = "Light"
