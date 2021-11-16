from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('students/', views.generate_product_info),
    path('', RedirectView.as_view(url='students/', permanent=True)),
]