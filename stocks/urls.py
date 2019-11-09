from django.urls import path
from . import views

app_name = 'stocks'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('details/', views.DetailView.as_view(), name='detail'),
    path('search_price/', views.search_price, name='search_price'),
    path('price/', views.PriceChartView.as_view(), name='price'),
    path('search_fcf/', views.search_cashflow, name='search_cashflow'),
    path('fcf/', views.FCFPSChartView.as_view(), name='cashflow'),

]
