import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLineEdit, QPushButton


class TableFilterDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.table_widget = QTableWidget(5, 3)
        self.table_widget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])

        # Fill the table with example data
        data = [
            ["Apple", "Banana", "Cherry"],
            ["Avocado", "Blueberry", "Coconut"],
            ["Almond", "Blackberry", "Date"],
            ["Apricot", "Blackcurrant", "Fig"],
            ["Asparagus", "Broccoli", "Grape"]
        ]

        for row in range(len(data)):
            for col in range(len(data[row])):
                self.table_widget.setItem(row, col, QTableWidgetItem(data[row][col]))

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Enter text to filter Column 2")

        self.filter_button = QPushButton("Apply Filter")
        self.filter_button.clicked.connect(self.apply_filter)

        layout = QVBoxLayout()
        layout.addWidget(self.filter_input)
        layout.addWidget(self.filter_button)
        layout.addWidget(self.table_widget)

        self.setLayout(layout)
        self.setWindowTitle("QTableWidget Column Filtering Example")
        self.resize(400, 300)

    def apply_filter(self):
        filter_text = self.filter_input.text().lower()
        column_index = 1  # Index of the column to filter (0-based index)

        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, column_index)
            if item:
                if filter_text in item.text().lower():
                    self.table_widget.setRowHidden(row, False)
                else:
                    self.table_widget.setRowHidden(row, True)
            else:
                self.table_widget.setRowHidden(row, True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = TableFilterDemo()
    demo.show()
    sys.exit(app.exec_())
