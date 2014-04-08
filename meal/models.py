from django.db import models

# Create your models here.
class Meal(models.Model):
	name = models.CharField("Name of Meal",max_length=200)
	date_created = models.DateTimeField("Created Date",auto_now_add=True)
	date_modified = models.DateTimeField("Modified Date",auto_now=True)
	
	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField("Name of Product",max_length=200)
	date_created = models.DateTimeField("Created Date",auto_now_add=True)
	date_modified = models.DateTimeField("Modified Date",auto_now=True)

	def __str__(self):
		return self.name

class Stock(models.Model):
	amount = models.FloatField("Amount of Product in Stock", null=True)
	count = models.IntegerField("Count of Product in Stock", null=True)
	product = models.ForeignKey(Product, verbose_name="Related Product")
	date_created = models.DateTimeField("Created Date",auto_now_add=True)
	date_modified = models.DateTimeField("Modified Date",auto_now=True)

	def __str__(self):
		return "Product Name: " + self.product.name + " Amount: " + str(self.amount) + " Count: " + str(self.count)

class Ingredient(models.Model):
	meal = models.ForeignKey(Meal, verbose_name="Related Meal")
	product = models.ForeignKey(Product, verbose_name="Related Product")
	amount = models.FloatField("Amount of Product in Meal",null=True)
	count = models.IntegerField("Count of Product in Meal",null=True)
	date_created = models.DateTimeField("Created Date",auto_now_add=True)
	date_modified = models.DateTimeField("Modified Date",auto_now=True)

	def __str__(self):
		return "Ingredients of Product: " + self.product.name + " Amount: " + str(self.amount) + " Count: " + str(self.count)