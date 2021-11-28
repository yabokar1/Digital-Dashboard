from django.shortcuts import render, redirect
from django.core import serializers
from django.http import JsonResponse
import json
from django.http import HttpResponse
from .models import Districts
from .utils import get_plot
from .forms import DistrictForm

def generate_product_info(request):
    return render(request, 'main.html')

def create_district_graph():
    form = DistrictForm()
    return form



def percentage_access_in_state(state):

    state_list = Districts.objects.filter(state=state)
    district_list = []
    county_connection = []
    for x in state_list:
        print("The district {}".format(state),x.county_connection)
        county_connection.append(x.county_connection)
        district_list.append(x.district_id)
        print("The county connection",county_connection)
        print("The district_id", district_list)

    return county_connection,district_list





def percentage_access_black_hispanic(request):
    states = ['Utah', 'Illinois', 'Wisconsin', 'NC', 'Missouri', 'Washington', 'Massachusetts', 'NY', 'Indiana',
              'Virginia', 'New Jersey', 'DOC', 'Texas']

    Utah = []
    Illi = []
    Wisco = []
    mean_perc = []
    north = []
    miss = []
    wash = []
    connect = []
    mass = []
    newyork = []
    indiana = []
    vir = []
    ohio = []
    jersey = []
    cal = []
    dis = []
    ari = []
    tex = []

    obj = Districts.objects.all()

    for district_info in obj:
        if district_info.state == 'Utah':
            Utah.append(district_info.pct_black_hispanic)

        elif district_info.state == 'Illinois':
            Illi.append(district_info.pct_black_hispanic)
        elif district_info.state == 'Wisconsin':
            Wisco.append(district_info.pct_black_hispanic)
        elif district_info.state == 'North Carolina':
            north.append(district_info.pct_black_hispanic)
        elif district_info.state == 'Missouri':
            miss.append(district_info.pct_black_hispanic)
        elif district_info.state == 'Washington':
            wash.append(district_info.pct_black_hispanic)
        elif district_info.state == 'Connecticut':
            connect.append(district_info.pct_black_hispanic)
        elif district_info.state == 'Massachusetts':
            mass.append(district_info.pct_black_hispanic)
        elif district_info.state == 'New York':
            newyork.append(district_info.pct_black_hispanic)
        elif district_info.state == 'Indiana':
            indiana.append(district_info.pct_black_hispanic)
        elif district_info.state == 'Virginia':
            vir.append(district_info.pct_black_hispanic)
        elif district_info.state == 'Ohio':
            ohio.append(district_info.pct_black_hispanic)
        elif district_info.state == 'New Jersey':
            jersey.append(district_info.pct_black_hispanic)
        elif district_info.state == 'California':
            cal.append(district_info.pct_black_hispanic)
        elif district_info.state == 'District Of Columbia':
            dis.append(district_info.pct_black_hispanic)
        elif district_info.state == 'Arizona':
            ari.append(district_info.pct_black_hispanic)
        elif district_info.state == 'Texas':
            tex.append(district_info.pct_black_hispanic)

    mean_perc.append((sum(Utah)) / len(Utah))
    #mean_perc.append((sum(Illi)) / len(Illi))
    mean_perc.append((sum(Wisco)) / len(Wisco))
    mean_perc.append((sum(north)) / len(north))
    mean_perc.append((sum(miss)) / len(miss))
    mean_perc.append((sum(wash)) / len(wash))
    mean_perc.append((sum(mass)) / len(mass))
    mean_perc.append((sum(newyork)) / len(newyork))
    mean_perc.append((sum(indiana)) / len(indiana))
    mean_perc.append((sum(vir)) / len(vir))
    mean_perc.append((sum(jersey)) / len(jersey))
    mean_perc.append((sum(dis)) / len(dis))
    mean_perc.append((sum(tex)) / len(tex))


    final_state_list = json.dumps(states)
    final_mean_perc_list = json.dumps(mean_perc)

    form = create_district_graph()
    county, district = percentage_access_in_state("Illinois")

    if request.method == 'POST':
        form = DistrictForm(request.POST)
        if form.is_valid():
            input_state = form.cleaned_data['state']

            print("The state is",input_state)
            county,district = percentage_access_in_state(input_state)
            print("The county is",county)
            print("The district is",district)

            return render(request, 'index.html', {'district': district, 'county': county, 'form': form, 'state':final_state_list , 'perc': final_mean_perc_list})

    print("The request post is",request.POST)
    return render(request, 'index.html', {'state':final_state_list , 'perc': final_mean_perc_list, 'form': form})

