from PyQt5 import QtChart, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from collections import namedtuple
from functools import partial
from db import transactiondb
import random


class MyChart(QtChart.QChart):
    def __init__(self, datas, parent=None):
        super().__init__()
        super(MyChart, self).__init__(parent)
        self.__datas = datas
        self.legend().hide()
        self.setAnimationOptions(QtChart.QChart.SeriesAnimations)

        self.outer = QtChart.QPieSeries()
        self.inner = QtChart.QPieSeries()
        self.outer.setHoleSize(0.35)
        self.inner.setPieSize(0.35)
        self.inner.setHoleSize(0.3)

        self.set_outer_series()
        self.set_inner_series()

        self.addSeries(self.outer)
        self.addSeries(self.inner)

    def set_outer_series(self):
        slices = list()
        for data in self.__datas:
            print(data.name[0])
            print(data.value)
            slice_ = QtChart.QPieSlice(data.name[0], data.value)
            slice_.setLabelVisible()
            slice_.setColor(data.primary_color)
            slice_.setLabelBrush(data.primary_color)

            slices.append(slice_)
            self.outer.append(slice_)

        # label styling
        for slice_ in slices:
            color = 'black'
            if slice_.percentage() > 0.1:
                slice_.setLabelPosition(QtChart.QPieSlice.LabelInsideHorizontal)
                color = 'white'

            label = "<p align='center' style='color:{}'>{}<br>{}%</p>".format(
                color,
                slice_.label(),
                round(slice_.percentage() * 100, 2)
            )
            slice_.setLabel(label)
            slice_.hovered.connect(partial(self.explode, slice_))

    def set_inner_series(self):
        for data in self.__datas:
            slice_ = self.inner.append(data.name[0], data.value)
            slice_.setColor(data.secondary_color)
            slice_.setBorderColor(data.secondary_color)

    def explode(self, slice_, is_hovered):
        if is_hovered:
            start = slice_.startAngle()
            end = slice_.startAngle() + slice_.angleSpan()
            self.inner.setPieStartAngle(end)
            self.inner.setPieEndAngle(start + 360)
        else:
            self.inner.setPieStartAngle(0)
            self.inner.setPieEndAngle(360)

        slice_.setExplodeDistanceFactor(0.1)
        slice_.setExploded(is_hovered)


class DashboardWidget(QWidget):

    def __init__(self, parent=None):
        super(DashboardWidget, self).__init__(parent)
        self.setFixedSize(QtCore.QSize(700, 400))
        Data = namedtuple('Data', ['name', 'value', 'primary_color', 'secondary_color'])

        category = transactiondb.get_category()
        total_expense = transactiondb.get_total_expense()
        datas = []
        if category:
            for i in category:
                color, light = self.get_color()
                total_amount = transactiondb.get_category_transactions(i[0])
                if total_amount == None:
                    continue
                else:
                    cat = Data(name=i, value=total_amount, primary_color=QtGui.QColor(color), secondary_color=QtGui.QColor(light))
                    datas.append(cat)


        chart = MyChart(datas)

        chart_view = QtChart.QChartView(chart)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(chart_view)

    def get_color(self):
        red = random.randint(129, 255)
        green = random.randint(129, 255)
        blue = random.randint(129, 255)
        lred = red//2
        lgreen = green//2
        lblue = blue//2

        # Format the color in hexadecimal representation
        color = "#{:02x}{:02x}{:02x}".format(red, green, blue)
        light_color ="#{:02x}{:02x}{:02x}".format(lred, lgreen, lblue)
        return color, light_color

    def modeChange(self, state):
        if state:
            pass
        else:
            pass
