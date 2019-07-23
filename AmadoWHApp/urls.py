from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('sendsms', views.sendsms,name='sendsms'),
    path('getform', views.getform,name='getform'),
    path('', views.report,name='report'),
    path('getprices', views.get_prices,name='get_prices'),
    path('branchvar/<int:id>/', views.branchvar,name='branchvar'),
    path('branchvarsum/<int:id>/', views.branchvarsum,name='branchvarsum'),
]