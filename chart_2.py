from PyQt5 import QtCore, QtWidgets, QtGui, QtChart
import math, random


class ChartThing(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        # print("hello world")

        # make the line chart in the widget
        series = QtChart.QLineSeries()
        for i in range(100):
            series.append((random.random()-0.5)**3, i)

        chart = QtChart.QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.legend().hide()

        chartView = QtChart.QChartView(chart)

        self.setCentralWidget(chartView)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ChartThing()
    window.resize(400, 500)
    window.show()
    sys.exit(app.exec_())