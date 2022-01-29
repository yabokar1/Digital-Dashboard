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
from .forms import FilterForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required


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


            return HttpResponseRedirect('/dashboard/home',{'form' : form})

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


def show_join_us_page(request):
    return render(request, 'joinustoday.html')


def show_sign_up_page(request):
    return render(request, 'sign-up.html')

def generate_product_info(request):
    return render(request, 'main.html')

def create_district_graph():
    # form = DistrictForm()
    form = FilterForm
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
    states = ['Utah', 'Illinois', 'Wisconsin', 'North Carolina', 'Missouri', 'Washington', 'Connecticut', 'Massachusetts', 'New York', 'Indiana', 'Virginia', 'Ohio', 'New Jersey', 'California', 'District of Columbia', 'Arizona','Texas']

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

    # final_states_list = json.dumps(states)
    # final_expenditure_list = json.dumps(avg_expenditure_for_states)    #commenting lines 212 and 213 for now
    return states,avg_expenditure_for_states


def totalNumberOfSchoolDistricts():
    district_ids = []
    states = []
    obj = Districts.objects.all()
    for item in obj:
        if item.district_id and item.district_id not in district_ids:
            district_ids.append(item.district_id)
        if item.state and item.state not in states:
            states.append(item.state);
    return len(district_ids), len(states)

def total_number_of_products():
    product_list = ProductsInfo.objects.filter()
    product_data = []

    for product in product_list:
        product_data.append({ "product_name": product.product_name, "url": product.url })

    return product_data, len(product_data)

def total_locale_type():
    suburb = Districts.objects.filter(locale="Suburb")
    rural = Districts.objects.filter(locale="Rural")
    town = Districts.objects.filter(locale="Town")
    city = Districts.objects.filter(locale="City")

    suburb_list = []
    rural_list = []
    town_list = []
    city_list = []
    for item in suburb:
        suburb_list.append(item)

    for item in rural:
        rural_list.append(item)

    for item in town:
         town_list.append(item)

    for item in city:
        city_list.append(item)

    return len(suburb_list), len(rural_list), len(town_list), len(city_list)


def avg(li):
    j = 0
    for i in li:
        j = j + i
    return (j/len(li))

@login_required(login_url='/dashboard/accounts/login/') 
def show_graphs_for_users(request):
    # userObject = UserProfile.objects.filter(user_id=request.user.id)
   logged_in_user_type = request.user.userprofile.user_type
   print('Logged in user type is',logged_in_user_type )
   print('This statement is',logged_in_user_type == 'student')
   if (logged_in_user_type == 'student'):
       return HttpResponseRedirect('/dashboard/student/')
   elif (logged_in_user_type == 'educator'):
       #call educator methods here
       print('Hi educator')
       return HttpResponseRedirect('/dashboard/speedtest/')

      #forces user to login if they try to go /dashboard/home path

@login_required(login_url='/dashboard/accounts/login/') 
def percentage_access_black_hispanic(request):
    states = ['Utah', 'Illinois', 'Wisconsin', 'NC', 'Missouri', 'Washington', 'Massachusetts', 'NY', 'Indiana',
              'Virginia', 'New Jersey', 'Texas', 'DOC']
    location_list = []

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

    keyVal = {};
    originalData = []   # Data contains array of objects

    i = 0
    for i in range(len(s)):
        originalData.append({ "state": s[i], "expenditure": exp[i] });
    
    data = json.dumps(originalData)              # data in JSON format ready to be used by d3.js

    numberofdistricts, numberofstates = totalNumberOfSchoolDistricts()         # statistic 1
    print('Total number of districts is', numberofdistricts)

    products, numberofproducts = total_number_of_products()                    #statistic 2

    suburb, rural, town, city = total_locale_type()

    if request.method == 'POST':
        # form = DistrictForm(request.POST)
        form = FilterForm(request.POST)
        if form.is_valid():

            # input_state = form.cleaned_data['state']
            input_country = request.POST.get('country')
            print("The country is",input_country)

            # print('location list is ', location_list)
            input_location = ''
            if (request.POST.get('locations') != None) :
                 input_location = request.POST.get('locations')
                 print('input Location is', input_location)


            if input_country == 'usa':
                location_list = ['Utah', 'Illinois', 'Wisconsin', 'North Carolina', 'Missouri', 'Washington', 'Massachusetts', 'New York', 'Indiana',
              'Virginia', 'New Jersey', 'Texas', 'District of Columbia']
                if input_location:
                    #state related data
                    return render(request, 'state.html')
                else:
                    return render(request, 'index.html', {'district': district, 'county': county, 'form': form, 'state':final_state_list , 'perc': final_mean_perc_list , 'st':s, 'ex':exp, 'mydata': data, 'location_list': location_list, 'inputlocation': input_location, 'inputcountry': input_country, 'firststat': numberofdistricts, 'secondstat': numberofstates, 'thirdstat': numberofproducts, 'products': products, 'suburb': suburb, 'rural': rural, 'town': town, 'city': city })

            else:
                # need to check here if user selected only country or also a state, if country show overview, if state show state related graphs
                location_list = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador', 'Northwest Territories', 'Nova Scotia', 'Nunavut', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']
                # return render(request, 'sign-up.html')     # this is where we show canadian data

            

            # return render(request, 'index.html', {'district': district, 'county': county, 'form': form, 'state':final_state_list , 'perc': final_mean_perc_list , 'st':s, 'ex':exp, 'mydata': data, 'location_list': location_list, 'inputlocation': input_location, 'inputcountry': input_country, 'firststat': numberofdistricts })

    
    return render(request, 'index.html', {'state':final_state_list , 'perc': final_mean_perc_list, 'form': form, 'st':s, 'ex':exp, 'mydata': data, 'firststat': numberofdistricts, 'secondstat': numberofstates, 'thirdstat': numberofproducts, 'products': products, 'suburb': suburb, 'rural': rural, 'town': town, 'city': city})

