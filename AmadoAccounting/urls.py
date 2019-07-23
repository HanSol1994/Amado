from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('uploadsalary', views.upload_salary,name='upload_salary'),
]