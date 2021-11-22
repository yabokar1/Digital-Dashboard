from django.urls import path
from . import views
from django.shortcuts import render
from django.views.generic import RedirectView

urlpatterns = [
    path('students/', views.percentage_access_black_hispanic),
    path('', RedirectView.as_view(url='students/', permanent=True)),
]