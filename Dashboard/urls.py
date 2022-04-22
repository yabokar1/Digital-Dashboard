from django.urls import path, include
from django.shortcuts import render
from django.views.generic import RedirectView
from django.contrib import admin
from . import views
from .view import canadianviews
from .view import apiviews





urlpatterns = [
    
    path('users/login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('students/login', views.getStudent),
    path("ethnicity/", views.usa_ethnicity),
    path("expenditure/", views.usa_expenditure),
    path("county_connection/", views.usa_county_connection),
    path("statistics/", views.usa_statistics),
    path("top_engagement/", views.usa_top_10_product_engagement),
    path("bottom_engagement/", views.usa_bottom_10_product_engagement),
    path("broadband/", views.usa_broadband),
    path("engagement_info/", views.usa_product_engagement_info),
    path("free_reduced/", views.usa_free_reduced),
    path("engagement_info/<str:pk>", views.usa_free_reduced),
    path("county_connection/<str:pk>", views.usa_free_reduced),
   
     path('twitter/', views.getTweets),
   


    path('home/', views.show_graphs_for_users),
    path('student/', views.percentage_access_black_hispanic),
    path('researcher/', views.views_for_researcher),
    path('join-us-today/', views.show_join_us_page),
    path('wifihotspots/', views.show_wifi_hotspots_information),
    path('statcollector/', views.stat_collector_page),
    # path('login/', views.show_user_login__page),
    path('art/', views.canadian_data),
    path('pdfgenerator/', views.show_pdf_page),
    path('graphgenerator/', views.show_file_upload_csv_page),
    path('pdf-summaries/', views.show_pdf_summary_extractor_page),
    path('signup/', views.create_user_for_signup),
    path('accounts/', include('django.contrib.auth.urls')),
    path('speedtest/', views.show_speed_test_page),
    path('canadian/', views.canadian_data),
    path('mentalhealth/', views.mentalhealth),
    path('interactivedashboard/', views.show_interactive_dashboard_page),
    path('participation/', views.participation_rate),
    path('labour/', views.labour_force),
    path('enrollment/', views.post_enrollment),
    path('expenditure/', views.expenditure_college),
    path('apprentice/', views.apprentice_registration),
    path('unemployment/', views.unemployment_rate),
    path('testscore/', views.test_score),
    path('loadsummaries/', views.data_for_pdf_summary_extractor_page_api_call),
    path('students/', views.studentPage),
    
    path('', RedirectView.as_view(url='join-us-today/', permanent=True)),   # change here and change in settings.py
    path('admin/',admin.site.urls)

]