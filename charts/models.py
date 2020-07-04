from django.db import models
import yfinance as yf
import plotly
import plotly.graph_objects as go

class Stock(models.Model):

	INTERVAL_CHOICES = [
		    ('1m','1 Minute'),
		    ('5m','5 Minute'),
		    ('15m','15 Minute'),
		    ('30m','30 Minute'),
		    ('1h','Hourly'),
		    ('1d','Daily'),
		    ('1wk','Weekly'),
		    ('1mo','Monthly'),
		    ('1y','Yearly'),
		    ('max','Maximum')
		]

	name = models.CharField(max_length=200)
	symbol = models.CharField(max_length=15)
	period = models.CharField(max_length=5,choices=INTERVAL_CHOICES,default='1mo')
	is_index = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	def get_stock_info(self):
		tick = yf.Ticker(self.symbol)
		info = {
			'id':self.id,
			'name':tick.info['shortName'],
			'symbol':self.symbol,
			'close':tick.info['previousClose'],
			'diff': round(tick.info['regularMarketOpen']-tick.info['previousClose'],3)
		}
		return info

	def get_stock_data(self,period=""):
		tick = yf.Ticker(self.symbol)
		if not period:
			period = self.period
		if str(period) in ['1wk','1mo','1y']:
			data = tick.history(interval=period,period="1y")
		else:
			data = tick.history(interval=period,period="1mo")
		return data

	def get_candle_figure(self,data):
		graph_fig = go.Figure(data=[go.Candlestick(
			x=list(data.index),
			open=data['Open'],
			high=data['High'],
			low=data['Low'],
			close=data['Close'],
			increasing_line_color= 'cyan',
			decreasing_line_color= 'white',
			)])
		graph_fig.update_layout(
			xaxis_rangeslider_visible=False,
			font=dict(
			        size=12,
			        color="white"
			    ),
			paper_bgcolor='rgba(0,0,0,0)',
    		plot_bgcolor='rgba(0,0,0,0)'
			)
		return graph_fig

	def get_line_figure(self,data):
		line_fig = go.Figure(data=[go.Scatter(x=list(data.index),y=data['Close'],mode='lines',fill='tonexty',line_color='aqua')])
		line_fig.update_layout(
			yaxis_title="Close",
			font=dict(
			        size=12,
			        color="white"
			    ),
			paper_bgcolor='rgba(0,0,0,0)',
    		plot_bgcolor='rgba(0,0,0,0)'
			)
		return line_fig
