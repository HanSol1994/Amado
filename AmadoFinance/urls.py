from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('cashpayment', views.view_cash,name='view_cash'),
    path('supplierreport', views.supplier_report,name='supplier_report'),
]