from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QComboBox, QHBoxLayout)
from db import transactiondb
import csv
import pandas as pd


class ExportComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExportComboBox, self).__init__(parent)

        # Remove the dropdown arrow
        self.setStyleSheet("QComboBox::drop-down { border: 0; }")

        # Add items to the combobox
        self.addItem("To CSV")
        self.addItem("To Excel")


class ReportsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        hlayout = QHBoxLayout()
        export_label = QLabel("Export Transactions:")
        self.combo_box = ExportComboBox(self)
        generate_button = QPushButton("Generate")
        hlayout.addWidget(export_label)
        hlayout.addWidget(self.combo_box)
        layout.addLayout(hlayout)
        layout.addWidget(generate_button)
        generate_button.clicked.connect(self.export_report)
        with open('ui/stylesheets/light/reports.css', 'r') as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

    def export_report(self):
        rows, desc = transactiondb.export_transactions()
        header = [description[0] for description in desc]
        print(header)
        report_type = self.combo_box.currentText()
        if report_type == "To CSV":
            csv_file_path = 'D:/output.csv'
            with open(csv_file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)

                csv_writer.writerow(header)

                # Write rows
                csv_writer.writerows(rows)

            print(f'CSV file created at: {csv_file_path}')

        elif report_type == "To Excel":
            excel_file_path = 'D:/output_excel.xlsx'
            df = pd.DataFrame(rows, columns=header)
            print(df)
            df.to_excel(excel_file_path, index=False)

    def modeChange(self, state):
        if state:
            with open('ui/stylesheets/dark/reportsDark.css', 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        else:
            with open('ui/stylesheets/light/reports.css', 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
