from django.shortcuts import render

# Create your views here.


def educator_home_page(request):
    return render(request, 'main.html')