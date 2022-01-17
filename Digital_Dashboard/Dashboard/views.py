from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core import serializers
from django.http import JsonResponse
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, ProfileForm

from .models import Districts
from .models import ProductsInfo
from .models import EngagementInfo
from .forms import DistrictForm


def create_user_for_signup(request):

    if(request.method == 'POST'):
        form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if(form.is_valid() and profile_form.is_valid()):
            
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            print("The username is",username)
            print("The password is",raw_password)
            user = authenticate(username=username, password=raw_password)
            login(request, user)


            return HttpResponseRedirect('/dashboard',{'form' : form})

        else:
            # return HttpResponseRedirect('/dashboard/signup',{'form' : form})
            print(form.errors)
        
    else:
        form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'sign-up.html', {'form' : form, 'profile_form': profile_form})
        

def show_speed_test_page(request):
    return render(request, 'speed-test.html')  

def show_user_login__page(request):
    return render(request, 'login.html')


def show_sign_up_page(request):
    return render(request, 'sign-up.html')

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
        # print("The district {}".format(state),x.county_connection)
        county_connection.append(x.county_connection)
        district_list.append(x.district_id)
        # print("The county connection",county_connection)
        # print("The district_id", district_list)

    return county_connection,district_list


def expenditure_per_pupil_in_different_states():
    avg_expenditure_for_states = []
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
    states = ['Utah', 'Illinois', 'Wisconsin', 'NC', 'Missouri', 'Washington', 'Connecticut', 'Massachusetts', 'NY', 'Indiana', 'Virginia', 'Ohio', 'New Jersey', 'California', 'DOC', 'Arizona','Texas']

    o = Districts.objects.all()

    for item in o:
        if item.state == 'Utah':
            Utah.append(item.pp_total_raw)
        elif item.state == 'Illinois':
            Illi.append(item.pp_total_raw)
        elif item.state == 'Wisconsin':
            Wisco.append(item.pp_total_raw)
        elif item.state == 'North Carolina':
            north.append(item.pp_total_raw)
        elif item.state == 'Missouri':
            miss.append(item.pp_total_raw)
        elif item.state == 'Washington':
            wash.append(item.pp_total_raw)
        elif item.state == 'Connecticut':
            connect.append(item.pp_total_raw)
        elif item.state == 'Massachusetts':
            mass.append(item.pp_total_raw)
        elif item.state == 'New York':
            newyork.append(item.pp_total_raw)
        elif item.state == 'Indiana':
            indiana.append(item.pp_total_raw)
        elif item.state == 'Virginia':
            vir.append(item.pp_total_raw)
        elif item.state == 'Ohio':
            ohio.append(item.pp_total_raw)
        elif item.state == 'New Jersey':
            jersey.append(item.pp_total_raw)
        elif item.state == 'California':
            cal.append(item.pp_total_raw)
        elif item.state == 'District Of Columbia':
            dis.append(item.pp_total_raw)
        elif item.state == 'Arizona':
            ari.append(item.pp_total_raw)
        elif item.state == 'Texas':
            tex.append(item.pp_total_raw)

    if len(Utah) > 0:
        avg_expenditure_for_states.append(avg(Utah))
    else:
        avg_expenditure_for_states.append(0)
    if len(Illi) > 0:
        avg_expenditure_for_states.append(avg(Illi))
    else:
        avg_expenditure_for_states.append(0)
    if len(Wisco) > 0:
        avg_expenditure_for_states.append(avg(Wisco))
    else:
        avg_expenditure_for_states.append(0)
    if len(north) > 0:
        avg_expenditure_for_states.append(avg(north))
    else:
        avg_expenditure_for_states.append(0)
    if len(miss) > 0:
        avg_expenditure_for_states.append(avg(miss))
    else:
        avg_expenditure_for_states.append(0)
    if len(wash) > 0:
        avg_expenditure_for_states.append(avg(wash))
    else:
        avg_expenditure_for_states.append(0)
    if len(connect) > 0:
        avg_expenditure_for_states.append(avg(connect))
    else:
        avg_expenditure_for_states.append(0)
    if len(mass) > 0:
        avg_expenditure_for_states.append(avg(mass))
    else:
        avg_expenditure_for_states.append(0)
    if len(newyork) > 0:
        avg_expenditure_for_states.append(avg(newyork))
    else:
        avg_expenditure_for_states.append(0)
    if len(indiana) > 0:
        avg_expenditure_for_states.append(avg(indiana))
    else:
        avg_expenditure_for_states.append(0)
    if len(vir) > 0:
        avg_expenditure_for_states.append(avg(vir))
    else:
        avg_expenditure_for_states.append(0)
    if len(ohio) > 0:
        avg_expenditure_for_states.append(avg(ohio))
    else:
        avg_expenditure_for_states.append(0)
    if len(jersey) > 0:
        avg_expenditure_for_states.append(avg(jersey))
    else:
        avg_expenditure_for_states.append(0)
    if len(cal) > 0:
        avg_expenditure_for_states.append(avg(cal))
    else:
        avg_expenditure_for_states.append(0)
    if len(dis) > 0:
        avg_expenditure_for_states.append(avg(dis))
    else:
        avg_expenditure_for_states.append(0)
    if len(ari) > 0:
        avg_expenditure_for_states.append(avg(ari))
    else:
        avg_expenditure_for_states.append(0)
    if len(tex) > 0:
        avg_expenditure_for_states.append(avg(tex))
    else:
        avg_expenditure_for_states.append(0)

    final_states_list = json.dumps(states)
    final_expenditure_list = json.dumps(avg_expenditure_for_states)
    return final_states_list,final_expenditure_list


def avg(li):
    j = 0
    for i in li:
        j = j + i
    return (j/len(li))

def percentage_access_black_hispanic(request):
    states = ['Utah', 'Illinois', 'Wisconsin', 'NC', 'Missouri', 'Washington', 'Massachusetts', 'NY', 'Indiana',
              'Virginia', 'New Jersey', 'Texas', 'DOC']

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
    s = []
    exp = []

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
    mean_perc.append((sum(Illi)) / len(Illi))
    mean_perc.append((sum(Wisco)) / len(Wisco))
    mean_perc.append((sum(north)) / len(north))
    mean_perc.append((sum(miss)) / len(miss))
    mean_perc.append((sum(wash)) / len(wash))
    mean_perc.append((sum(mass)) / len(mass))
    mean_perc.append((sum(newyork)) / len(newyork))
    mean_perc.append((sum(indiana)) / len(indiana))
    mean_perc.append((sum(vir)) / len(vir))
    mean_perc.append((sum(jersey)) / len(jersey))
    mean_perc.append((sum(tex)) / len(tex))
    mean_perc.append((sum(dis)) / len(dis))
    
    final_state_list = json.dumps(states)
    final_mean_perc_list = json.dumps(mean_perc)
    # print("The list is ",final_state_list)
    # print("The perc list is ",final_mean_perc_list)

    s, exp = expenditure_per_pupil_in_different_states()
    print("Expenditure is",exp)
    form = create_district_graph()
    county, district = percentage_access_in_state("Illinois")

    if request.method == 'POST':
        form = DistrictForm(request.POST)
        if form.is_valid():
            input_state = form.cleaned_data['state']

            # print("The state is",input_state)
            county,district = percentage_access_in_state(input_state)
            # print("The county is",county)
            # print("The district is",district)

            return render(request, 'index.html', {'district': district, 'county': county, 'form': form, 'state':final_state_list , 'perc': final_mean_perc_list , 'st':s, 'ex':exp})

    # print("The request post is",request.POST)
    return render(request, 'index.html', {'state':final_state_list , 'perc': final_mean_perc_list, 'form': form, 'st':s, 'ex':exp})

