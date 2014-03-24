from django.db import models

# Create your models here.
class Meal(models.Model):
	name = models.CharField(max_length=200)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

class Product(models.Model):
	name = models.CharField(max_length=200)
	barcode = models.CharField(max_length=200)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

class Stock(models.Model):
	amount = models.FloatField()
	count = models.IntegerField()
	product = models.ForeignKey(Product)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

class Ingredient(models.Model):
	meal = models.ForeignKey(Meal)
	product = models.ForeignKey(Product)
	amount = models.FloatField()
	count = models.IntegerField()
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)