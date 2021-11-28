from django.urls import path
from . import views


urlpatterns = [

    path('',views.educator_home_page,name='educator'),

]