from django.urls import path

from . import views

app_name = 'charts'
urlpatterns =[
	path('', views.index, name='index'),
	path('search/', views.search, name='search'),
	path('analysis/<int:stock_id>/', views.analysis, name='analysis'),
	path('news/<int:stock_id>/', views.news, name='news'),
	path('info/<int:stock_id>/', views.info, name='info'),
	path('download/<int:stock_id>/', views.download, name='download'),
]