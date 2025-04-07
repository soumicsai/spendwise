from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QScrollArea,
                             QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QSizePolicy,
                             QLabel, QDateEdit, QComboBox)
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QDate
from db import transactiondb, tablecreate
from ui import budgets

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

class TransactionWindow(QWidget):
    content_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        transaction_layout = QVBoxLayout()
        categoryLabel = QLabel("Category:")
        amountLabel = QLabel("Amount:")
        dateLabel = QLabel("Date:")
        okButton = QPushButton("Add Transaction")
        self.category_edit = QComboBox()
        category_list = transactiondb.get_category()
        for category in category_list:
            self.category_edit.addItem(category[0])
        self.amount_edit = QLineEdit()
        self.date_edit = QDateEdit()
        today = QDate.currentDate()
        self.date_edit.setDate(today)
        okButton.clicked.connect(self.add_trans)
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(categoryLabel)
        hlayout1.addWidget(self.category_edit)
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(amountLabel)
        hlayout2.addWidget(self.amount_edit)
        hlayout3 = QHBoxLayout()
        hlayout3.addWidget(dateLabel)
        hlayout3.addWidget(self.date_edit)
        transaction_layout.addLayout(hlayout1)
        transaction_layout.addLayout(hlayout2)
        transaction_layout.addLayout(hlayout3)
        transaction_layout.addWidget(okButton)
        self.setLayout(transaction_layout)

    def add_trans(self):
        category = self.category_edit.currentText()
        amount = self.amount_edit.text()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        l1 = [category, amount, date]
        tablecreate.connection_to_db()
        transactiondb.insert_transaction(l1)
        self.content_changed.emit(l1)
        category_Widget = budgets.BudgetsWidget.li[category]
        budgets.CategoryWidget.set_progress(category_Widget, category_name=category)
        self.close()

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
            self.transaction_list.setHorizontalHeaderLabels(["Category", "Amount", "Date"])
            self.transaction_list.setRowCount(0)
            for i in records:
                self.multi_column_list_item(i)
        else:
            self.transaction_list.clear()
            self.transaction_list.setHorizontalHeaderLabels(["Category", "Amount", "Date"])
            self.transaction_list.setRowCount(0)

    def reinsert(self, records):
        if records:
            self.transaction_list.clear()
            self.transaction_list.setHorizontalHeaderLabels(["Category", "Amount", "Date"])
            self.transaction_list.setRowCount(0)
            for i in records:
                self.multi_column_list_item(i)
        else:
            transactions = transactiondb.show_transactions()
            if transactions:
                for i in transactions:
                    self.multi_column_list_item(i)

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
