from django.urls import path

from . import views

app_name = 'charts'
urlpatterns =[
	path('', views.index, name='index'),
	path('search/', views.search, name='search'),
	path('dashboard/<int:stock_id>/', views.dashboard, name='dashboard'),
	path('news/<int:stock_id>/', views.news, name='news'),
	path('info/<int:stock_id>/', views.info, name='info'),
]