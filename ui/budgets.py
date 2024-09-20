from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QVBoxLayout,
                             QPushButton, QGroupBox, QLabel, QProgressBar, QHBoxLayout, QLineEdit, QDialog, QComboBox,
                             QMessageBox, QApplication, QScrollArea)

from db import transactiondb
from db import budgetsdb
from ui import window


class CategoryWindow(QWidget):
    category_added = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        category_window_layout = QVBoxLayout()
        category_label = QLabel("Category")
        budget_label = QLabel("Budget")
        self.category_edit = QLineEdit()
        self.budget_edit = QLineEdit()
        group_layout1 = QHBoxLayout()
        group_layout1.addWidget(category_label)
        group_layout1.addWidget(self.category_edit)
        group_layout2 = QHBoxLayout()
        group_layout2.addWidget(budget_label)
        group_layout2.addWidget(self.budget_edit)
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_category)
        category_window_layout.addLayout(group_layout1)
        category_window_layout.addLayout(group_layout2)
        category_window_layout.addWidget(add_button)
        self.setLayout(category_window_layout)

    def add_category(self):
        category = self.category_edit.text()
        budget = self.budget_edit.text()
        budgetsdb.insert_categories(category)
        budgetsdb.insert_budget(category, budget)
        self.category_added.emit('category added')
        self.close()


class CategoryWidget(QWidget):
    def __init__(self, category_name):
        super().__init__()
        self.category_name = category_name
        category_layout = QHBoxLayout()
        category_label = QLabel(category_name.capitalize() + ' :')
        self.category_budget_progress = QProgressBar()
        self.category_budget_progress.setMaximum(100)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_budget_progress)
        self.setLayout(category_layout)
        self.setWindowTitle('Add Category')
        self.set_progress(self.category_name)

    def set_progress(self, category_name):
        budget = budgetsdb.get_budget(category_name)
        used_amt = transactiondb.get_category_transactions(category_name)
        if used_amt is None:
            budget_per = 0
        else:
            budget_per = (used_amt * 100) // budget
        self.category_budget_progress.setValue(budget_per)
        self.update()


class BudgetsWidget(QWidget):
    li = {}

    def __init__(self):
        super().__init__()
        self.category_popup_window = None
        self.budget_progress_layout = None
        self.budget_group = QGroupBox('Budgets')
        self.budget_layout = QVBoxLayout(self)
        self.scroll_budget = QScrollArea(self)
        self.scroll_budget.setWidgetResizable(True)
        self.init_ui()

    def init_ui(self):
        if transactiondb.get_total_expense():
            total_expense = transactiondb.get_total_expense()
            total_budget = budgetsdb.total_budgets()
        else:
            total_expense = 0
            total_budget = 0

        total_budget_label = QLabel(f"Total : ${total_budget}")
        total_spent_label = QLabel(f"Spent : ${total_expense}")
        add_category_button = QPushButton("Add Category")
        budget_group_layout = QVBoxLayout()
        budget_list_widget = QWidget(self)
        self.scroll_budget.setWidget(budget_list_widget)
        self.budget_progress_layout = QVBoxLayout(budget_list_widget)
        budget_group_layout.addWidget(self.scroll_budget)
        budget_group_layout.addWidget(add_category_button)
        self.refresh()
        add_category_button.clicked.connect(self.category_window)
        self.budget_group.setLayout(budget_group_layout)
        self.budget_layout.addWidget(self.budget_group)
        budget_summary_layout = QVBoxLayout()
        budget_summary_layout.addWidget(total_budget_label)
        budget_summary_layout.addWidget(total_spent_label)
        self.budget_layout.addLayout(budget_summary_layout)
        with open('ui/stylesheets/light/budgets.css', 'r') as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

    def modeChange(self,state):
        if state:
            with open('ui/stylesheets/dark/budgetsDark.css', 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        else:
            with open('ui/stylesheets/light/budgets.css', 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)

    def category_window(self):
        icon = QtGui.QIcon("resources/ico/icon.ico")
        self.category_popup_window = CategoryWindow()
        self.category_popup_window.setWindowIcon(icon)
        self.category_popup_window.setGeometry(500, 500, 544, 400)
        self.category_popup_window.show()
        self.category_popup_window.category_added.connect(self.updateLayout)

    def refresh(self):
        self.li.clear()
        category_list = transactiondb.get_category()
        if category_list:
            for category in category_list:
                category1 = CategoryWidget(category[0])
                self.li[category[0]] = category1
                self.budget_progress_layout.addWidget(category1)

    def updateLayout(self):
        for i in reversed(range(self.budget_progress_layout.count())):
            widgetToRemove = self.budget_progress_layout.itemAt(i).widget()
            if isinstance(widgetToRemove, CategoryWidget):
                self.budget_progress_layout.removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)
        self.refresh()
