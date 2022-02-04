from django.urls import path, include
from . import views
from django.shortcuts import render
from django.views.generic import RedirectView

urlpatterns = [
    path('home/', views.show_graphs_for_users),
    path('student/', views.percentage_access_black_hispanic),
    path('join-us-today/', views.show_join_us_page),
    path('wifihotspots/', views.show_wifi_hotspots_information),
    path('statcollector/', views.stat_collector_page),
    # path('login/', views.show_user_login__page),
    path('signup/', views.create_user_for_signup),
    path('accounts/', include('django.contrib.auth.urls')),
    path('speedtest/', views.show_speed_test_page),
    path('', RedirectView.as_view(url='join-us-today/', permanent=True)),   # change here and change in settings.py
]