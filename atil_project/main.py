import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from webcam import readBarcode

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		uic.loadUi('meal_suggestion.ui', self)
		self.show()
		self.tabWidget3.setCurrentIndex(0)
		self.tabWidget3.currentChanged.connect(self.changeTab)
		self.actionRead_Barcode_from_Webcam.triggered.connect(self.readFromWebCam)
		self.actionAbout_Meal_Suggestion.triggered.connect(self.aboutApp)
	def changeTab(self, index):
		print "New Index %i" %(index)
	def readFromWebCam(self):
		symbol = ""
		counter = 0
		while (symbol == ""):
			symbol = readBarcode()
			counter += 1
			if counter >= 20:
				break
		if symbol == "":
			QMessageBox.about(self, "Webcam Image Alert", "We couldn't find any good image to read!!!")
		else:
			QMessageBox.about(self, "Webcam Barcode Result", symbol)
	def aboutApp(self):
		QMessageBox.about(self, "Meal Suggestion Application", "Can Atil CTIS@2014")

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec_())