from django.shortcuts import render_to_response, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_POST
from django.core.context_processors import csrf
from django.http import HttpResponse
from meal.models import *
from datetime import datetime
import json

# Create your views here.
def view_meals_suggestion(request):
	c = {"meals":Meal.objects.all()}
	c.update(csrf(request))
	return render_to_response("home.html", c)

@require_POST
def show_meal_stock(request):
	meal = get_object_or_404(Meal, id=int(request.POST['meal_id']))
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
	return HttpResponse(json.dumps(return_data), content_type="application/json")