from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages


# pk_e09dd775c1cf4c44b6ab8120de862117

def home(request):
	import requests
	import json


	if request.method == 'POST':

		ticker = request.POST['ticker']

		if ticker == "":
			messages.warning(request, ("No symbol entered"))
			return render(request, 'home.html', {})

		

		api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_e09dd775c1cf4c44b6ab8120de862117")

		try:
			api = json.loads(api_requests.content)

		except Exception as e:
			api = "Error . . ."

		return render(request, 'home.html', {'api': api})

	else:
		return render(request, 'home.html', {'ticker': "Please enter a symbol for look up!"})

	

def about(request):
	return render(request, 'about.html', {})

def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, ("Stock was added to portfolio" ))
			return redirect('add_stock')
	else:
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:
			api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_e09dd775c1cf4c44b6ab8120de862117")
			try:
				api = json.loads(api_requests.content)
				api.update({'tickerid': ticker_item.id})
				output.append(api)
			except Exception as e:
				api = "Error . . ."
		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock with symbol [ " +  item.ticker +     " ] was removed from portfolio") )
	return redirect(add_stock)

def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker} )



