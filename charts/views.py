from django.shortcuts import get_object_or_404,render
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from .models import Stock

from bs4 import BeautifulSoup
import requests
import plotly
import plotly.graph_objects as go
import urllib.parse

def index(request):
	return render(request, 'charts/home.html',{})

def dashboard(request,stock_id):
	period = request.GET.get('period')
	stock = get_object_or_404(Stock, pk=stock_id)

	if period:
		data = stock.get_stock_data(period)
	else:
		data = stock.get_stock_data()

	bar_fig = go.Figure(data=[go.Bar(y=data['Volume'],x=list(data.index),marker_color="aqua")])
	bar_fig.update_layout(
			yaxis_title="Volume",
			font=dict(
					size=12,
					color="white"
				),
			paper_bgcolor='rgba(0,0,0,0)',
			plot_bgcolor='rgba(0,0,0,0)'
			)
	bar_div = bar_fig.to_html(full_html=False, default_height=350)

	graph_fig = stock.get_candle_figure(data)
	graph_div = graph_fig.to_html(full_html=False, default_height=500)

	line_fig = stock.get_line_figure(data)
	line_div = line_fig.to_html(full_html=False, default_height=350)
	return render(request, 'charts/dashboard.html',
		{
		'stock':stock,
		'info':stock.get_stock_info(),
		'graph_div':graph_div,
		'line_div':line_div,
		'bar_div':bar_div
		})

def news(request,stock_id):
	stock = get_object_or_404(Stock, pk=stock_id)
	url = "https://in.finance.yahoo.com/quote/"+urllib.parse.quote(str(stock.symbol))
	print(url)
	response = requests.get(url)
	page_content = BeautifulSoup(response.content, "html.parser")
	headings = page_content.find_all("h3",attrs={"class":"Mb(5px)"})
	contents = page_content.find_all("p")
	headings = [h.text for h in headings]
	contents = [c.text for c in contents]
	print(len(headings))
	news = {}
	for i in range(len(headings)):
		news.update({headings[i]:contents[i]})
	return render(request, 'charts/news.html',
		{
		'stock':stock,
		'info':stock.get_stock_info(),
		'news':news
		})

def info(request,stock_id):
	stock = get_object_or_404(Stock, pk=stock_id)
	return render(request, 'charts/info.html',
		{
		'stock':stock,
		'info':stock.get_stock_info()
		})

def search(request):
	search_word = str(request.GET.get('search_query'))
	s_list=[]
	if search_word:
		s_list = Stock.objects.filter(
			Q(name__icontains=search_word) | Q(symbol__icontains=search_word)
		)
	
	if not s_list:
		s_list = Stock.objects.all()

	content = []
	
	for stock in s_list:
		content.append(stock.get_stock_info())
		
	return render(request, 'charts/stock_search.html',
		{
		'content':content,
		})
