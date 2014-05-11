import sys
import settings
import random
from datetime import datetime
from meal.models import *
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from barcode import getBarcode
from button import getButton

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		uic.loadUi('meal_suggestion.ui', self)
		self.show()
		self.tabWidget3.setCurrentIndex(0)
		self.tabWidget3.currentChanged.connect(self.changeTab)
		self.actionRead_Barcode_from_Webcam.triggered.connect(self.readFromWebCam)
		self.actionAbout_Meal_Suggestion.triggered.connect(self.aboutApp)
		self.actionCheck_Stock.triggered.connect(self.checkDateOfStock)
		self.pushButton.clicked.connect(self.addMeal)
		self.pushButton_2.clicked.connect(self.addProduct)
		self.pushButton_3.clicked.connect(self.addStock)
		self.pushButton_4.clicked.connect(self.addRecipe)
		self.pushButton_5.clicked.connect(self.suggestMeal)
		self.pushButton_6.clicked.connect(self.checkMeal)
		self.pushButton_7.clicked.connect(self.deleteStock)
		self.pushButton_9.clicked.connect(self.deleteProduct)
		self.readFromWebCamBtn.clicked.connect(self.readFromWebCamToBarcode)
		self.readFromWebCamBtn_2.clicked.connect(self.readFromWebCamToStock)
		self.setMealTableData()
		self.setProductTableData()
		self.setStockTableData()
		self.setIngredientTableData()
		self.setProductCombos()
		self.setMealCombo()
		self.setStockCombo()
	def changeTab(self, index):
		pass
	def readFromWebCam(self):
		symbol = getButton()
		if symbol == "":
			QMessageBox.about(self, "Button Alert", "We couldn't find button!!!")
		else:
			if symbol=="23":
				self.suggestMeal()
			elif symbol=="24":
				self.addProduct()
	def readFromWebCamToBarcode(self):
		symbol = getBarcode()
		if symbol == "":
			QMessageBox.about(self, "Barcode Alert", "We couldn't find barcode!!!")
		else:
			QMessageBox.about(self, "Barcode Found", "We just found the barcode!!!")
			self.lineEdit_3.setText(symbol)
	def readFromWebCamToStock(self):
		symbol = getBarcode()
		if symbol == "":
			QMessageBox.about(self, "Barcode Alert", "We couldn't find barcode!!!")
		else:
			QMessageBox.about(self, "Barcode Found", "We just found the barcode!!!")
			selected_products = Product.objects.filter(barcode=symbol)
			if len(selected_products) > 0:
				index = 0
				for p in Product.objects.all():
					if p.id == selected_products[0].id:
						self.comboBox.setCurrentIndex(index)
						break
					index += 1
			else:
				QMessageBox.about(self, "Product Not Found!", "Please add to Product before add new Stock!!!")
	def deleteFromBarcode(self):
		symbol = getBarcode()
		if symbol == "":
			QMessageBox.about(self, "Barcode Alert", "We couldn't find barcode!!!")
		else:
			QMessageBox.about(self, "Barcode Found", "We just found the barcode!!!")
			selected_products = Product.objects.filter(barcode=symbol)
			if len(selected_products) > 0:
				p = selected_products[0]
				index = self.comboBox.findItem(p.id)
				if index >= 0:
					self.comboBox.setCurrentIndex(index)
			else:
				QMessageBox.about(self, "Product Not Found!", "Please add to Product before add new Stock!!!")
	def deleteStock(self):
		item_data = self.comboBox_5.itemData(self.comboBox_5.currentIndex())
		stock = Stock.objects.get(id=int(item_data.toString()))
		stock.delete()
		self.setStockTableData()
		self.setStockCombo()
	def deleteProduct(self):
		item_data = self.comboBox_7.itemData(self.comboBox_7.currentIndex())
		product = Product.objects.get(id=int(item_data.toString()))
		product.delete()
		self.setProductTableData()
		self.setProductCombos()
	def checkDateOfStock(self):
		stocks = Stock.objects.filter(date_expired__lt=datetime.now())
		if(len(stocks) > 0):
			QMessageBox.about(self, "Some Stock are expired", "Please check your expired stocks!!!")
		else:
			QMessageBox.about(self, "Stock is fresh", "Stock is fresh and you can use for your meals!!!")
	def checkMeal(self):
		item_data = self.comboBox_4.itemData(self.comboBox_4.currentIndex())
		meal = Meal.objects.get(id=int(item_data.toString()))
		ingredients = meal.ingredient_set.all()
		isOK = True
		meal_needs = []
		for ing in ingredients:
			p = ing.product
			stocks = p.stock_set.filter(date_expired__gte=datetime.now())
			totalAmount = 0.0
			totalCount = 0
			for stock in stocks:
				totalAmount += stock.amount
				totalCount += stock.count
			if totalAmount == 0 and totalCount == 0:
				need = {"product":p.name, "amount_need":ing.amount, "count_need": ing.count}
				meal_needs.append(need)
				isOK = isOK & False
			if ing.amount > totalAmount or ing.count > totalCount:
				need = {"product":p.name, "amount_need":(ing.amount - totalAmount), "count_need": (ing.count - totalCount)}
				meal_needs.append(need)
				isOK = isOK & False
		return_data = {}
		if len(ingredients) == 0:
			return_data = {"result":False, "msg":"You should add some ingredients first"}
		else:
			if isOK:
				return_data = {"result":True, "msg":"Ok! You can make your meal with your current stock"}
			else:
				return_data= {"result":False, "needs":meal_needs, "msg":"You should buy new products for your meal!"}
		QMessageBox.about(self, "Check Meal", return_data["msg"])
	def suggestMeal(self):
		meals = Meal.objects.all()
		available_meals = []
		for meal in meals:
			ingredients = meal.ingredient_set.all()
			isOK = True
			for ing in ingredients:
				p = ing.product
				stocks = p.stock_set.filter(date_expired__gte=datetime.now())
				totalAmount = 0.0
				totalCount = 0
				for stock in stocks:
					totalAmount += stock.amount
					totalCount += stock.count
				if totalAmount == 0 and totalCount == 0:
					isOK = False
					break
				if ing.amount > totalAmount or ing.count > totalCount:
					isOK = False
					break
			if isOK:
				available_meals.append(meal)
		if len(available_meals) == 0:
			QMessageBox.about(self, "No Meal is Found", "No Meal is Found")
		else:
			rand_int = random.randint(0,len(available_meals) - 1)
			current_meal = available_meals[rand_int]
			reply = QtGui.QMessageBox.question(self, 'A Meal is Found: ' + current_meal.name, 
                     'Would you like to order the ' + current_meal.name, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.Yes:
				ingredients = current_meal.ingredient_set.all()
				five_years_later = datetime.now().replace(year = datetime.now().year + 5)
				for ing in ingredients:
					stock = Stock(product=ing.product,amount=ing.amount * -1,count=ing.count * -1,date_expired=five_years_later)
					stock.save()
				self.setStockTableData()				
	def aboutApp(self):
		QMessageBox.about(self, "Meal Suggestion Application", "Can Atil Efe CTIS@2014")
	def setMealTableData(self):
		self.tableWidget_4.clear()
		meals = Meal.objects.all()
		row = 0
		self.tableWidget_4.setRowCount(len(meals))
		self.tableWidget_4.setColumnCount(1)
		self.tableWidget_4.setHorizontalHeaderItem(0,QTableWidgetItem("Meal Name"))
		for meal in meals:
			meal_name = QTableWidgetItem(meal.name)
			meal_name.setFlags(Qt.ItemIsEnabled)
			self.tableWidget_4.setItem(row,0,meal_name)
			row += 1
	def setProductTableData(self):
		self.tableWidget.clear()
		products = Product.objects.all()
		row = 0
		self.tableWidget.setRowCount(len(products))
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderItem(0,QTableWidgetItem("Product Name"))
		self.tableWidget.setHorizontalHeaderItem(1,QTableWidgetItem("Barcode"))
		for product in products:
			product_name = QTableWidgetItem(product.name)
			product_name.setFlags(Qt.ItemIsEnabled)
			self.tableWidget.setItem(row,0,product_name)
			product_barcode = QTableWidgetItem(product.barcode)
			product_barcode.setFlags(Qt.ItemIsEnabled)
			self.tableWidget.setItem(row,1,product_barcode)
			row += 1
	def setStockTableData(self):
		self.tableWidget_2.clear()
		self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
		stocks = Stock.objects.all()
		row = 0
		self.tableWidget_2.setRowCount(len(stocks))
		self.tableWidget_2.setColumnCount(4)
		self.tableWidget_2.setHorizontalHeaderItem(0,QTableWidgetItem("Product Name"))
		self.tableWidget_2.setHorizontalHeaderItem(1,QTableWidgetItem("Amount"))
		self.tableWidget_2.setHorizontalHeaderItem(2,QTableWidgetItem("Count"))
		self.tableWidget_2.setHorizontalHeaderItem(3,QTableWidgetItem("Expired Date"))
		for stock in stocks:
			stock_name = QTableWidgetItem(stock.product.name)
			stock_name.setFlags(Qt.ItemIsEnabled)
			self.tableWidget_2.setItem(row,0,stock_name)
			stock_amount = QTableWidgetItem(str(stock.amount))
			stock_amount.setFlags(Qt.ItemIsEnabled)
			self.tableWidget_2.setItem(row,1,stock_amount)
			stock_count = QTableWidgetItem(str(stock.count))
			stock_count.setFlags(Qt.ItemIsEnabled)
			self.tableWidget_2.setItem(row,2,stock_count)
			stock_expired_date = QTableWidgetItem(str(stock.date_expired))
			stock_expired_date.setFlags(Qt.ItemIsEnabled)
			self.tableWidget_2.setItem(row,3,stock_expired_date)
			row += 1
	def setIngredientTableData(self):
		self.tableWidget_3.clear()
		ingredients = Ingredient.objects.all()
		row = 0
		self.tableWidget_3.setRowCount(len(ingredients))
		self.tableWidget_3.setColumnCount(4)
		self.tableWidget_3.setHorizontalHeaderItem(0,QTableWidgetItem("Meal Name"))
		self.tableWidget_3.setHorizontalHeaderItem(1,QTableWidgetItem("Product Name"))
		self.tableWidget_3.setHorizontalHeaderItem(2,QTableWidgetItem("Amount"))
		self.tableWidget_3.setHorizontalHeaderItem(3,QTableWidgetItem("Count"))
		for ingredient in ingredients:
			ing_meal_name = QTableWidgetItem(ingredient.meal.name)
			ing_meal_name.setFlags(Qt.ItemIsEnabled)
			self.tableWidget_3.setItem(row,0,ing_meal_name)

			ing_product_name = QTableWidgetItem(ingredient.product.name)
			ing_product_name.setFlags(Qt.ItemIsEnabled)
			self.tableWidget_3.setItem(row,1,ing_product_name)

			ing_amount = QTableWidgetItem(str(ingredient.amount))
			ing_amount.setFlags(Qt.ItemIsEnabled)
			self.tableWidget_3.setItem(row,2,ing_amount)

			ing_count = QTableWidgetItem(str(ingredient.count))
			ing_count.setFlags(Qt.ItemIsEnabled)
			self.tableWidget_3.setItem(row,3,ing_count)
			row += 1
	def setProductCombos(self):
		self.comboBox.clear()
		self.comboBox_2.clear()
		self.comboBox_7.clear()
		for product in Product.objects.all():
			self.comboBox.addItem(product.name, product.id)
			self.comboBox_2.addItem(product.name, product.id)
			self.comboBox_7.addItem(product.name, product.id)
	def setMealCombo(self):
		self.comboBox_3.clear()
		self.comboBox_4.clear()
		for meal in Meal.objects.all():
			self.comboBox_3.addItem(meal.name, meal.id)
			self.comboBox_4.addItem(meal.name, meal.id)
	def setStockCombo(self):
		self.comboBox_5.clear()
		for stock in Stock.objects.all():
			self.comboBox_5.addItem(stock.product.name + " " + str(stock.date_expired), stock.id)
	def addMeal(self):
		if self.lineEdit.text() != "":
			new_meal = Meal(name=self.lineEdit.text())
			new_meal.save()
			self.lineEdit.setText("")
			self.setMealCombo()
			self.setMealTableData()
		else:
			QMessageBox.about(self, "Meal Name Empty", "Please fill the meal name!!!")
	def addProduct(self):
		temp_var = self.dateEdit.date() 
		expired_date = temp_var.toPyDate()
		if self.lineEdit_2.text() != "" and self.lineEdit_3.text() != "":
			new_product = Product(name=self.lineEdit_2.text(), barcode=self.lineEdit_3.text())
			new_product.save()
			self.lineEdit_2.setText("")
			self.lineEdit_3.setText("")
			self.setProductCombos()
			self.setProductTableData()
		else:
			QMessageBox.about(self, "Product Name or Barcode Empty", "Please fill the product name and barcode!!!")
	def addStock(self):
		temp_var = self.dateEdit.date()
		expired_date = temp_var.toPyDate()
		if (self.spinBox.value() > 0 or self.doubleSpinBox.value() > 0.0) and (self.comboBox.count() > 0) and datetime(expired_date.year, expired_date.month, expired_date.day) > datetime.now():
			selected_product = Product.objects.all()[self.comboBox.currentIndex()]
			new_stock = Stock(product=selected_product,count=self.spinBox.value(),
								amount=self.doubleSpinBox.value(), date_expired = expired_date)
			new_stock.save()
			self.spinBox.setValue(0)
			self.doubleSpinBox.setValue(0.0)
			self.setStockTableData()
			self.setStockCombo()
		else:
			QMessageBox.about(self, "Wrong Amount or Count Value or Expired Date is Wrong", "Check your values!!!")
	def addRecipe(self):
		if (self.spinBox_2.value() > 0 or self.doubleSpinBox_2.value() > 0.0) and self.comboBox_2.count() > 0 and self.comboBox_3.count() > 0:
			selected_product = Product.objects.all()[self.comboBox_2.currentIndex()]
			selected_meal = Meal.objects.all()[self.comboBox_3.currentIndex()]
			new_ing = Ingredient(product=selected_product,count=self.spinBox_2.value(),
								amount=self.doubleSpinBox_2.value(),meal=selected_meal)
			new_ing.save()
			self.spinBox_2.setValue(0)
			self.doubleSpinBox_2.setValue(0.0)
			self.setIngredientTableData()
		else:
			QMessageBox.about(self, "Wrong Amount or Count Value", "Amount or Count should be larger than zero!!!")

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec_())