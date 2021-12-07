from django.urls import path, include
from . import views
from django.shortcuts import render
from django.views.generic import RedirectView

urlpatterns = [
    path('home/', views.percentage_access_black_hispanic),
    # path('login/', views.show_user_login__page),
    path('signup/', views.create_user_for_signup),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url='home/', permanent=True)),
]