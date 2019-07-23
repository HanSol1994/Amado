from django.urls import path
from django.shortcuts import redirect
from . import views


urlpatterns = [
    path('calch', views.calch,name='calculate_home'),
    path('calcacl2', views.calc_ac_l2,name='calculate_acost_lvl2'),
    path('calcacl3', views.calc_ac_l3,name='calculate_acost_lvl3'),


]