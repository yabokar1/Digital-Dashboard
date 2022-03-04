import math

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import json
import requests
import numpy as np
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, ProfileForm
from .models import Districts
from .models import ProductsInfo
from .models import EngagementInfo
from .forms import FilterForm
from .models import StudentFormInfo
from .models import RatingInfo
from .models import CountyConnectionInfo
from django.contrib.auth.decorators import login_required
from random import randint

from operator import itemgetter

names_of_places = []
library_places = []
rating_star_list = []

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
            print(form.errors)
        
    else:
        form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'sign-up.html', {'form' : form, 'profile_form': profile_form})

def stat_collector_page(request):
    student_province = ""
    school_grade = 0
    test_score = 0
    attendance_percentage = 0
    student_device = ""
    workstatus = ""
    parent_salary = ""
    wifi_present = ""
    wifi_company = ""
    wifi_speed = ""

    if (request.method == 'POST'):
        student_province =  request.POST.get('province')
        school_grade = int(request.POST.get('grade'))
        if (request.POST.get('testscore')):
            test_score = int(request.POST.get('testscore'))
        attendance_percentage = int(request.POST.get('attendance'))
        student_device = (request.POST.get('device'))
        workstatus = request.POST.get('studentstatus')
        parent_salary = request.POST.get('parentsstatus')
        wifi_present = request.POST.get('wifi')

        if (request.POST.get('wificompany')):
            wifi_company = request.POST.get('wificompany')
        
        if (request.POST.get('wifispeed')):
            wifi_speed = request.POST.get('wifispeed')
        print("student_province is", student_province)
        print("school_grade is", school_grade)
        print("test_score is", test_score)
        print("attendance_percentage is", attendance_percentage)
        print("student_devices is", student_device)
        print("workstatus is", workstatus)
        print("parent_salary is", parent_salary)
        print("wifi_present is", wifi_present)
        print("wifi_company is", wifi_company)
        print("wifi_speed is", wifi_speed)

    if (student_province != "" and school_grade != "" and attendance_percentage != "" ):
        StudentFormInfo.objects.create(province=student_province,schoolgrade=school_grade, testscore=test_score,attendancepercentage=attendance_percentage,device=student_device,studentworkstatus=workstatus,parentssalary=parent_salary,wifi=wifi_present, wificompany=wifi_company,wifispeed=wifi_speed)  
    return render(request, 'informationcollector.html')

def show_wifi_hotspots_information(request):
    input_address = ''
    names_of_places.clear()
    library_places.clear();
    in_latitude = ''
    in_longitude = ''
    userRating = ''
    qualityOfWifi = ''
    placeName  = ''
    placeAddress = ''

    if (request.method == 'POST' and request.POST.get('ratingRange') and request.POST.get('wifiquality')):
        userRating = int(request.POST.get('ratingRange'))
        qualityOfWifi = int(request.POST.get('wifiquality'))
        placeName = request.POST.get('placename')
        placeAddress = request.POST.get('placeaddress')

        RatingInfo.objects.create(rating=userRating,wifiquality=qualityOfWifi,name=placeName, placeaddress=placeAddress)



    print('everything is',userRating,qualityOfWifi,placeName,placeAddress)
    show_wifi_hotspots_page(request, "cafe");
    show_wifi_hotspots_page(request, "library");

    if (request.method == 'POST'):
        input_address = request.POST.get('address')
        in_latitude = request.POST.get('cityLat')
        in_longitude = request.POST.get('cityLng')
    print("The address is", input_address)

    return render(request, 'wifihotspots.html', {'places' : names_of_places, 'libraries': library_places, 'address': input_address, 'lat': in_latitude, 'long': in_longitude})

def show_wifi_hotspots_page(request, type):
    latitude = ''
    longitude = ''
    payload={}
    headers = {}
    input_address = 'empty'
    rating = 0
    if request.method == 'POST' and request.POST.get('cityLat'):
        latitude = request.POST.get('cityLat')
        longitude = request.POST.get('cityLng')
        opening_hours = ""
        open_period = ""
        random_number = 0;
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+latitude+"%2C"+longitude+"&radius=10000&type="+type+"&key=AIzaSyDxQOJK5g7J9P6z9xXHq2hEt7zQMRxlspg";
        response = requests.request("GET", url, headers=headers, data=payload)
        json_data = json.loads(response.text)
        json_results = json_data["results"];

        ratingInfo = RatingInfo.objects.all()
        for i in range(len(json_results)):
            if (json_results[i].get("opening_hours") and json_results[i].get("opening_hours").get("open_now")):
                opening_hours = json_results[i].get("opening_hours").get("open_now")
            else:
                opening_hours = "Not listed"
            random_number = randint(10000, 99999); 
           
            for items in ratingInfo:
                if(items.name == json_results[i]["name"] and items.placeaddress in json_results[i]["vicinity"]):
                    print('isequal', items.placeaddress,json_results[i]["vicinity"])
                    rating = items.rating
                     
                    if type == 'cafe':                     
                        names_of_places.append({'name':json_results[i]["name"], 'vicinity': json_results[i]["vicinity"], 'isOpen': opening_hours, 'rating': rating, 'id': random_number})
                        if ({'name':json_results[i]["name"], 'vicinity': json_results[i]["vicinity"], 'isOpen': opening_hours, 'rating': "No rating found", 'id': random_number} in names_of_places):
                            names_of_places.remove({'name':json_results[i]["name"], 'vicinity': json_results[i]["vicinity"], 'isOpen': opening_hours, 'rating': "No rating found", 'id': random_number})
                    elif (type == 'library'):
                        library_places.append({'name':json_results[i]["name"], 'vicinity': json_results[i]["vicinity"], 'isOpen': opening_hours, 'rating': rating, 'id': random_number})
                        if ({'name':json_results[i]["name"], 'vicinity': json_results[i]["vicinity"], 'isOpen': opening_hours, 'rating': "No rating found", 'id': random_number} in library_places):
                            library_places.remove({'name':json_results[i]["name"], 'vicinity': json_results[i]["vicinity"], 'isOpen': opening_hours, 'rating': "No rating found", 'id': random_number})

                elif (items.name != json_results[i]["name"] or items.placeaddress not in json_results[i]["vicinity"]):
                    if type == 'cafe' and {'name':json_results[i]["name"], 'vicinity': json_results[i]["vicinity"], 'isOpen': opening_hours, 'rating': "No rating found", 'id': random_number} not in names_of_places and {'name':json_results[i]["name"], 'vicinity': json_results[i]["vicinity"], 'isOpen': opening_hours, 'rating': rating, 'id': random_number} not in names_of_places:                     
                        names_of_places.append({'name':json_results[i]["name"], 'vicinity': json_results[i]["vicinity"], 'isOpen': opening_hours, 'rating': "No rating found", 'id': random_number})
                    elif type == 'library' and {'name':json_results[i]["name"], 'vicinity': json_results[i]["vicinity"], 'isOpen': opening_hours, 'rating': "No rating found", 'id': random_number} not in library_places and {'name':json_results[i]["name"], 'vicinity': json_results[i]["vicinity"], 'isOpen': opening_hours, 'rating': rating, 'id': random_number} not in library_places:
                        library_places.append({'name':json_results[i]["name"], 'vicinity': json_results[i]["vicinity"], 'isOpen': opening_hours, 'rating': "No rating found", 'id': random_number})


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
        county_connection.append(x.county_connection)
        district_list.append(x.district_id)


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
    states = ['Utah', 'Illinois', 'Wisconsin', 'North Carolina', 'Missouri', 'Washington', 'New York', 'Indiana', 'Virginia', 'New Jersey','Texas']

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
        # elif item.state == 'Connecticut':
        #     connect.append(item.pp_total_raw)
        # elif item.state == 'Massachusetts':
        #     mass.append(item.pp_total_raw)
        elif item.state == 'New York':
            newyork.append(item.pp_total_raw)
        elif item.state == 'Indiana':
            indiana.append(item.pp_total_raw)
        elif item.state == 'Virginia':
            vir.append(item.pp_total_raw)
        # elif item.state == 'Ohio':
        #     ohio.append(item.pp_total_raw)
        elif item.state == 'New Jersey':
            jersey.append(item.pp_total_raw)
        # elif item.state == 'California':
        #     cal.append(item.pp_total_raw)
        # elif item.state == 'District Of Columbia':
            dis.append(item.pp_total_raw)
        # elif item.state == 'Arizona':
        #     ari.append(item.pp_total_raw)
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
    # # if len(connect) > 0:
    # #     avg_expenditure_for_states.append(avg(connect))
    # else:
    #     avg_expenditure_for_states.append(0)
    # if len(mass) > 0:
    #     avg_expenditure_for_states.append(avg(mass))
    # else:
    #     avg_expenditure_for_states.append(0)
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
    # if len(ohio) > 0:
    #     avg_expenditure_for_states.append(avg(ohio))
    # else:
    #     avg_expenditure_for_states.append(0)
    if len(jersey) > 0:
        avg_expenditure_for_states.append(avg(jersey))
    else:
        avg_expenditure_for_states.append(0)
    # if len(cal) > 0:
    #     avg_expenditure_for_states.append(avg(cal))
    # else:
    #     avg_expenditure_for_states.append(0)
    # if len(dis) > 0:
    #     avg_expenditure_for_states.append(avg(dis))
    # else:
    #     avg_expenditure_for_states.append(0)
    # if len(ari) > 0:
    #     avg_expenditure_for_states.append(avg(ari))
    # else:
    #     avg_expenditure_for_states.append(0)
    if len(tex) > 0:
        avg_expenditure_for_states.append(avg(tex))
    else:
        avg_expenditure_for_states.append(0)


    return states,avg_expenditure_for_states


def productEngagement():
    obj = EngagementInfo.objects.all().order_by('-engagement_index')

    for x in obj:
        print("I am are", x.lp_id, x.engagement_index)
    products = ProductsInfo.objects.all()
    products_data = []
    consumer_products = []
    unique_products = []
    products_array = []
    single_products_array = []
    single_average_engagement_array = []
    products_with_least_engagement_array = []
    least_engagement_array = []

    for x in obj:
        for product in products:
            if x.lp_id == product.lpid:
                products_data.append({'name': product.product_name, 'engagement': x.engagement_index})

    print('product data is', products_data)
    for dic in products_data:
        for key in (dic.keys()):
            if key == 'name':
                consumer_products.append(dic[key])
    unique_products = set(consumer_products)
    print(unique_products)

    for p in unique_products:
        average = 0
        count = 0
        for dict in products_data:
            if dict['name'] == p:
                average = average + dict['engagement']
                print('GS', p, average)
                count = count + 1
        products_array.append({'name': p, 'avg': average / count})

    print(products_array)

    top10products = sorted(products_array, key=itemgetter('avg'), reverse=True)[0:10]

    least10products = sorted(products_array, key=itemgetter('avg'), reverse=True)[-15:-5]
    print("least 10 is ", least10products)

    for item in top10products:
        for key, value in item.items():
            if key == 'name':
                single_products_array.append(value)
            elif key == 'avg':
                single_average_engagement_array.append(value)

    for p in least10products:
        for k, v in p.items():
            if k == 'name':
                products_with_least_engagement_array.append(v)
            elif k == 'avg':
                least_engagement_array.append(v)

    return products_with_least_engagement_array, least_engagement_array, single_products_array, single_average_engagement_array


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


def free_reduced():
    district = Districts.objects.all()
    free_reduce = {}
    avg_free_reduced = []

    for x in district:
        if x.state not in free_reduce:
            free_reduce[x.state] = []
        else:
            free_reduce[x.state].append(x.free_reduced)
    states = list(free_reduce.keys())
    for state in states:
        free_reduce[state] = round(np.mean(free_reduce[state]),2)
    return free_reduce


def product_engage(lp_id):
    products = EngagementInfo.objects.filter(lp_id=lp_id)
    products_info = ProductsInfo.objects.filter(lpid=lp_id)
    district_engagement = dict()
    time = []
    engagement = []
    p_info = ''


    for product in products:
        engagement.append(product.engagement_index)
        time.append(product.timestamp)

    for info in products_info:
        p_info = info.product_name
        print(p_info)

    return engagement,time,p_info

def broadband_connection():
    broad_band = CountyConnectionInfo.objects.all()
    state_broadband = {}
    states = ['Utah', 'Illinois', 'Wisconsin', 'North Carolina', 'Missouri', 'Washington', 'Connecticut',
              'Massachusetts', 'New York', 'Indiana', 'Virginia', 'Ohio', 'New Jersey', 'California', 'Arizona',
              'Texas']
    for x in broad_band:
        if x.state not in state_broadband and x.state in states:
            state_broadband[x.state] = []
        elif x.state in states:
            state_broadband[x.state].append((x.county_code, x.ratio, x.county_name))
    for state in state_broadband.keys():
        if state in states:
            avg = 0.0
            for x, item, y in state_broadband[state]:
                if item != 0.0:
                    avg = avg + item
            if avg / (len(state_broadband[state]) + 1) != 0.0:
                state_broadband[state] = round(avg / (len(state_broadband[state]) + 1), 2)

    states = list(state_broadband.keys())
    print("The states", states)

    broadband_avg = list(state_broadband.values())
    return states, broadband_avg

def total_locale_type():
    suburb = Districts.objects.filter(locale="Suburb")
    rural = Districts.objects.filter(locale="Rural")
    town = Districts.objects.filter(locale="Town")
    city = Districts.objects.filter(locale="City")
    local_type = []

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

    local_type.append(len(suburb_list))
    local_type.append(len(rural_list))
    local_type.append(len(town_list))
    local_type.append(len(city_list))
    return len(suburb_list), len(rural_list), len(town_list), len(city_list), local_type


def avg(li):
    j = 0
    for i in li:
        j = j + i
    return (int(j/len(li)))

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

    # Removed Massachusetts,District of Columbia

    Utah = []
    Illi = []
    Wisco = []
    mean_perc = []
    north = []
    miss = []
    wash = []
    connect = []
    # mass = []
    newyork = []
    indiana = []
    vir = []
    ohio = []
    jersey = []
    cal = []
    # dis = []
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
        # elif district_info.state == 'Massachusetts':
        #     mass.append(district_info.pct_black_hispanic)
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
        elif district_info.state == 'Arizona':
            ari.append(district_info.pct_black_hispanic)
        elif district_info.state == 'Texas':
            tex.append(district_info.pct_black_hispanic)

    mean_perc.append(round((sum(Utah)) / len(Utah),2))
    mean_perc.append(round((sum(Illi)) / len(Illi),2))
    mean_perc.append(round((sum(Wisco)) / len(Wisco),2))
    mean_perc.append(round((sum(north)) / len(north),2))
    mean_perc.append(round((sum(miss)) / len(miss),2))
    mean_perc.append(round((sum(wash)) / len(wash),2))
    mean_perc.append(round((sum(newyork)) / len(newyork),2))
    mean_perc.append(round((sum(indiana)) / len(indiana),2))
    mean_perc.append(round((sum(vir)) / len(vir),2))
    mean_perc.append(round((sum(jersey)) / len(jersey),2))
    mean_perc.append(round((sum(tex)) / len(tex),2))
    
    final_state_list = json.dumps(states)
    final_mean_perc_list = json.dumps(mean_perc)


    

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

    suburb, rural, town, city,type_of_local = total_locale_type()

    bottomProducts, engagementOfLeastProducts, productsOnly, engagementOnly =  productEngagement()

    productsOnly = json.dumps(productsOnly)
    engagementOnly = json.dumps(engagementOnly)
    leastProductsOnly = json.dumps(bottomProducts)
    leastEngagementOnly = json.dumps(engagementOfLeastProducts)




    
    st, broadband_average = broadband_connection()
    states_for_broadband = json.dumps(st)
    average_for_broadband = json.dumps(broadband_average)

    engagement, time, product_info = product_engage(60825)
    engagement = json.dumps(engagement)
    time = json.dumps(time)
    product_info = json.dumps(product_info)


    reduced = free_reduced()


    reduced_values = list(reduced.values())
    reduced_keys = list(reduced.keys())
    for x, y in reduced.items():
        if math.isnan(y):
            print(":", y)
            reduced_values.remove(y)
            reduced_keys.remove(x)

    multiple_reduced_values = json.dumps(reduced_values[:len(mean_perc)])
    multiple_pct_ethic = json.dumps(mean_perc[:len(mean_perc)])
    multiple_state = json.dumps(reduced_keys[:len(mean_perc)])



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
                    return render(request, 'index.html', {'district': district, 'county': county, 'form': form, 'state':final_state_list , 'perc': final_mean_perc_list , 'st':s, 'ex':exp, 'mydata': data, 'location_list': location_list, 'inputlocation': input_location, 'inputcountry': input_country, 'firststat': numberofdistricts, 'secondstat': numberofstates, 'thirdstat': numberofproducts, 'products': products, 'suburb': suburb, 'rural': rural, 'town': town, 'city': city,
                                                          'engagement': engagement, 'product_info': product_info,'time':time,
                                                          'reduced_free': multiple_reduced_values,
                                                          "pct_free": multiple_pct_ethic,
                                                          'multiple_state': multiple_state,'lepro': leastProductsOnly, 'leeng': leastEngagementOnly
                                                          })

            else:
                # need to check here if user selected only country or also a state, if country show overview, if state show state related graphs
                location_list = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador', 'Northwest Territories', 'Nova Scotia', 'Nunavut', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']


            



    return render(request, 'index.html', {'state':final_state_list , 'perc': final_mean_perc_list, 'form': form, 'st':s, 'ex':exp, 'mydata': data, 'firststat': numberofdistricts, 'secondstat': numberofstates, 'thirdstat': numberofproducts, 'products': products, 'suburb': suburb, 'rural': rural, 'town': town, 'city': city, 'localtype':type_of_local , 'pro': productsOnly, 'engo': engagementOnly, 'stb': states_for_broadband,
                                          'avgb': average_for_broadband,'engagement': engagement, 'product_info': product_info,'time':time,
                                          'reduced_free': multiple_reduced_values, "pct_free": multiple_pct_ethic,
                                          'multiple_state': multiple_state,'lepro': leastProductsOnly, 'leeng': leastEngagementOnly
                                          })

