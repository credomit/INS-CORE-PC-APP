from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
import sys
from PyQt5.QtGui import QIcon, QPen
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtCore import Qt
 
 
 
class Window(QWidget):
    def __init__(self):
        super().__init__()
 
        # window requirements
        self.setGeometry(200,200,600,400)
        self.setWindowTitle("Creating PieChart")
        self.setWindowIcon(QIcon("python.png"))
 
        # change the color of the window
        self.setStyleSheet('background-color:red')
 
        #create pieseries
        series  = QPieSeries()
 
        #append some data to the series 
        series.append("Apple", 80)
        series.append("Banana", 70)
        series.append("Pear", 50)
        series.append("Melon", 80)
        series.append("Water Melon", 30)
        series.append("Water Melon", 40)
        series.append("Water Melon", 40)
        series.append("Water Melon", 40)
        series.append("Water Melon", 40)      
        series.append("Water Melon", 40)
 
 
        def s_hovered(current_slice):
        	for unhovered_slice  in series.slices():
        		if unhovered_slice != current_slice:
        			unhovered_slice.setExploded(False)
        			unhovered_slice.setLabelVisible(False)

        	current_slice.setExploded(True)
        	current_slice.setLabelVisible(True)
 	
        series.hovered.connect(s_hovered)
 
 
        #create QChart object
        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Fruits Pie Chart")
        chart.setTheme(QChart.ChartThemeDark)
 
        # create QChartView object and add chart in thier 
        chartview = QChartView(chart)
 
 
        vbox = QVBoxLayout()
        vbox.addWidget(chartview)
 
        self.setLayout(vbox)
 
 
 
App = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(App.exec())







