from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit,
                             QHBoxLayout, QPushButton,
                             QLabel, QDateEdit, QComboBox)
from PyQt5.QtCore import pyqtSignal, QDate
from db import transactiondb, tablecreate
from ui import budgets

class TransactionWindow(QWidget):
    content_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        transaction_layout = QVBoxLayout()
        nameLabel = QLabel("Name :")
        categoryLabel = QLabel("Category:")
        amountLabel = QLabel("Amount:")
        dateLabel = QLabel("Date:")
        okButton = QPushButton("Add Transaction")
        self.category_edit = QComboBox()
        category_list = transactiondb.get_category()
        for category in category_list:
            self.category_edit.addItem(category[0])
        self.name_edit = QLineEdit()
        self.amount_edit = QLineEdit()
        self.date_edit = QDateEdit()
        today = QDate.currentDate()
        self.date_edit.setDate(today)
        okButton.clicked.connect(self.add_trans)
        hlayout = QHBoxLayout()
        hlayout.addWidget(nameLabel)
        hlayout.addWidget(self.name_edit)
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(categoryLabel)
        hlayout1.addWidget(self.category_edit)
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(amountLabel)
        hlayout2.addWidget(self.amount_edit)
        hlayout3 = QHBoxLayout()
        hlayout3.addWidget(dateLabel)
        hlayout3.addWidget(self.date_edit)
        transaction_layout.addLayout(hlayout)
        transaction_layout.addLayout(hlayout1)
        transaction_layout.addLayout(hlayout2)
        transaction_layout.addLayout(hlayout3)
        transaction_layout.addWidget(okButton)
        self.setLayout(transaction_layout)

    def add_trans(self):
        name = self.name_edit.text()
        category = self.category_edit.currentText()
        amount = self.amount_edit.text()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        l1 = [name,category, amount, date]
        tablecreate.connection_to_db()
        transactiondb.insert_transaction(l1)
        self.content_changed.emit(l1)
        category_Widget = budgets.BudgetsWidget.li[category]
        budgets.CategoryWidget.set_progress(category_Widget, category_name=category)
        self.close()