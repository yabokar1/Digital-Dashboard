import math

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import json
import requests
import numpy as np
# from .models import LabourForce
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, ProfileForm
from .models import Districts
from .models import ProductsInfo
from .models import EngagementInfo
from .forms import FilterForm
from .models import StudentFormInfo
from .models import RatingInfo
from .models import CountyConnectionInfo
from .models import LabourForce
from .models import PostSecondaryEnrollment
from .models import ExpenditureColleges
from .models import ParticipationRate
from .models import UnemploymentRate
from .models import ApprenticeshipRegistration
from .models import AverageTestScores
from .view import covidviews

from django.contrib.auth.decorators import login_required
from random import randint

import stats_can
from stats_can import StatsCan

from operator import itemgetter

names_of_places = []
library_places = []
rating_star_list = []


def create_user_for_signup(request):
    if (request.method == 'POST'):
        form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if (form.is_valid() and profile_form.is_valid()):

            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect('/dashboard/home', {'form': form})

        else:
            print(form.errors)

    else:
        form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'sign-up.html', {'form': form, 'profile_form': profile_form})


def show_password_change_page(request):
    return render(request, '/registration/password_change_form.html')

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
        student_province = request.POST.get('province')
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

    if (student_province != "" and school_grade != "" and attendance_percentage != ""):
        StudentFormInfo.objects.create(province=student_province, schoolgrade=school_grade, testscore=test_score,
                                       attendancepercentage=attendance_percentage, device=student_device,
                                       studentworkstatus=workstatus, parentssalary=parent_salary, wifi=wifi_present,
                                       wificompany=wifi_company, wifispeed=wifi_speed)
    return render(request, 'informationcollector.html')


def show_wifi_hotspots_information(request):
    input_address = ''
    names_of_places.clear()
    library_places.clear();
    in_latitude = ''
    in_longitude = ''
    userRating = ''
    qualityOfWifi = ''
    placeName = ''
    placeAddress = ''

    if (request.method == 'POST' and request.POST.get('ratingRange') and request.POST.get('wifiquality')):
        userRating = int(request.POST.get('ratingRange'))
        qualityOfWifi = int(request.POST.get('wifiquality'))
        placeName = request.POST.get('placename')
        placeAddress = request.POST.get('placeaddress')

        RatingInfo.objects.create(rating=userRating, wifiquality=qualityOfWifi, name=placeName,
                                  placeaddress=placeAddress)

    show_wifi_hotspots_page(request, "cafe");
    show_wifi_hotspots_page(request, "library");

    if (request.method == 'POST'):
        input_address = request.POST.get('address')
        in_latitude = request.POST.get('cityLat')
        in_longitude = request.POST.get('cityLng')

    return render(request, 'wifihotspots.html',
                  {'places': names_of_places, 'libraries': library_places, 'address': input_address, 'lat': in_latitude,
                   'long': in_longitude})


def show_wifi_hotspots_page(request, type):
    latitude = ''
    longitude = ''
    payload = {}
    headers = {}
    input_address = 'empty'
    rating = 0
    if request.method == 'POST' and request.POST.get('cityLat'):
        latitude = request.POST.get('cityLat')
        longitude = request.POST.get('cityLng')
        opening_hours = ""
        open_period = ""
        random_number = 0;
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + latitude + "%2C" + longitude + "&radius=10000&type=" + type + "&key=AIzaSyDxQOJK5g7J9P6z9xXHq2hEt7zQMRxlspg";
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
                if (items.name == json_results[i]["name"] and items.placeaddress in json_results[i]["vicinity"]):
                    # print('isequal', items.placeaddress,json_results[i]["vicinity"])
                    rating = items.rating

                    if type == 'cafe':
                        names_of_places.append(
                            {'name': json_results[i]["name"], 'vicinity': json_results[i]["vicinity"],
                             'isOpen': opening_hours, 'rating': rating, 'id': random_number})
                        if ({'name': json_results[i]["name"], 'vicinity': json_results[i]["vicinity"],
                             'isOpen': opening_hours, 'rating': "No rating found",
                             'id': random_number} in names_of_places):
                            names_of_places.remove(
                                {'name': json_results[i]["name"], 'vicinity': json_results[i]["vicinity"],
                                 'isOpen': opening_hours, 'rating': "No rating found", 'id': random_number})
                    elif (type == 'library'):
                        library_places.append({'name': json_results[i]["name"], 'vicinity': json_results[i]["vicinity"],
                                               'isOpen': opening_hours, 'rating': rating, 'id': random_number})
                        if ({'name': json_results[i]["name"], 'vicinity': json_results[i]["vicinity"],
                             'isOpen': opening_hours, 'rating': "No rating found",
                             'id': random_number} in library_places):
                            library_places.remove(
                                {'name': json_results[i]["name"], 'vicinity': json_results[i]["vicinity"],
                                 'isOpen': opening_hours, 'rating': "No rating found", 'id': random_number})

                elif (items.name != json_results[i]["name"] or items.placeaddress not in json_results[i]["vicinity"]):
                    if type == 'cafe' and {'name': json_results[i]["name"], 'vicinity': json_results[i]["vicinity"],
                                           'isOpen': opening_hours, 'rating': "No rating found",
                                           'id': random_number} not in names_of_places and {
                        'name': json_results[i]["name"], 'vicinity': json_results[i]["vicinity"],
                        'isOpen': opening_hours, 'rating': rating, 'id': random_number} not in names_of_places:
                        names_of_places.append(
                            {'name': json_results[i]["name"], 'vicinity': json_results[i]["vicinity"],
                             'isOpen': opening_hours, 'rating': "No rating found", 'id': random_number})
                    elif type == 'library' and {'name': json_results[i]["name"],
                                                'vicinity': json_results[i]["vicinity"], 'isOpen': opening_hours,
                                                'rating': "No rating found",
                                                'id': random_number} not in library_places and {
                        'name': json_results[i]["name"], 'vicinity': json_results[i]["vicinity"],
                        'isOpen': opening_hours, 'rating': rating, 'id': random_number} not in library_places:
                        library_places.append({'name': json_results[i]["name"], 'vicinity': json_results[i]["vicinity"],
                                               'isOpen': opening_hours, 'rating': "No rating found",
                                               'id': random_number})


def show_speed_test_page(request):
    return render(request, 'speed-test.html')


def show_user_login__page(request):
    return render(request, 'login.html')


def show_join_us_page(request):
    return render(request, 'joinustoday.html')


def show_sign_up_page(request):
    return render(request, 'sign-up.html')


def search_feature(word):
    search_words = ('engagement', 'expenditure', 'product', 'school', 'schools', 'access', 'districts', 'broadband', 'internet', 'black')
    context = {}
    context.clear()

    if (word in search_words):
        if (word == 'expenditure'):
            states, expenditure = expenditure_per_pupil_in_different_states()
            context['states'] = states
            context['exp'] = expenditure
        if word == 'engagement' or word == 'product':
            bottomProducts, engagementOfLeastProducts, productsOnly, engagementOnly = productEngagement()
            
            context['highengproducts'] = productsOnly
            context['higheng'] = engagementOnly
            context['lowengproducts'] = bottomProducts
            context['loweng'] = engagementOfLeastProducts

        if word == 'product':
            products, numberofproducts = total_number_of_products()
            
            context['namesofproducts'] = products
            context['learningproductcount'] = numberofproducts

        if word == 'broadband' or word == 'internet':
            st, broadband_average = broadband_connection()
            context['statesforbroadband'] = st
            context['avgbroadband'] = broadband_average
        
    return context
    

def show_pdf_page(request):
     input_country = ''


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

     mean_perc.append(round((sum(Utah)) / len(Utah), 2))
     mean_perc.append(round((sum(Illi)) / len(Illi), 2))
     mean_perc.append(round((sum(Wisco)) / len(Wisco), 2))
     mean_perc.append(round((sum(north)) / len(north), 2))
     mean_perc.append(round((sum(miss)) / len(miss), 2))
     mean_perc.append(round((sum(wash)) / len(wash), 2))
     mean_perc.append(round((sum(newyork)) / len(newyork), 2))
     mean_perc.append(round((sum(indiana)) / len(indiana), 2))
     mean_perc.append(round((sum(vir)) / len(vir), 2))
     mean_perc.append(round((sum(jersey)) / len(jersey), 2))
     mean_perc.append(round((sum(tex)) / len(tex), 2))

     final_state_list = json.dumps(states)
     final_mean_perc_list = json.dumps(mean_perc)

     s, exp = expenditure_per_pupil_in_different_states()
    # print("Expenditure is",exp)
     form = create_district_graph()
     county, district = percentage_access_in_state("Illinois")

     keyVal = {};
     originalData = []  # Data contains array of objects

     i = 0
     for i in range(len(s)):
        originalData.append({"state": s[i], "expenditure": exp[i]});

     data = json.dumps(originalData)  # data in JSON format ready to be used by d3.js

     numberofdistricts, numberofstates = totalNumberOfSchoolDistricts()  # statistic 1
    # print('Total number of districts is', numberofdistricts)

     products, numberofproducts = total_number_of_products()  # statistic 2

     suburb, rural, town, city, type_of_local = total_locale_type()

     bottomProducts, engagementOfLeastProducts, productsOnly, engagementOnly = productEngagement()

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
            # print(":", y)
            reduced_values.remove(y)
            reduced_keys.remove(x)

     multiple_reduced_values = json.dumps(reduced_values[:len(mean_perc)])
     multiple_pct_ethic = json.dumps(mean_perc[:len(mean_perc)])
     multiple_state = json.dumps(reduced_keys[:len(mean_perc)])



     if request.method == 'POST':
        print('i am coming in here')
        # form = DistrictForm(request.POST)
        form = FilterForm(request.POST)
        if form.is_valid():

            # input_state = form.cleaned_data['state']
            input_country = request.POST.get('country')
            # print("The country is",input_country)

            # print('location list is ', location_list)
            input_location = ''
            if (request.POST.get('locations') != None):
                input_location = request.POST.get('locations')
                # print('input Location is', input_location)

            if input_country == 'usa':
                location_list = ['Utah', 'Illinois', 'Wisconsin', 'North Carolina', 'Missouri', 'Washington',
                                'Massachusetts', 'New York', 'Indiana',
                                'Virginia', 'New Jersey', 'Texas', 'District of Columbia']
                if input_location:
                    # state related data
                    return render(request, 'state.html')
                else:
                    return render(request, 'index.html',
                                {'district': district, 'county': county, 'form': form, 'state': final_state_list,
                                'perc': final_mean_perc_list, 'st': s, 'ex': exp, 'mydata': data,
                                'location_list': location_list, 'inputlocation': input_location,
                                'inputcountry': input_country, 'firststat': numberofdistricts,
                                'secondstat': numberofstates, 'thirdstat': numberofproducts, 'products': products,
                                'suburb': suburb, 'rural': rural, 'town': town, 'city': city,
                                'engagement': engagement, 'product_info': product_info, 'time': time,
                                'reduced_free': multiple_reduced_values,
                                "pct_free": multiple_pct_ethic,
                                'multiple_state': multiple_state, 'lepro': leastProductsOnly,
                                'leeng': leastEngagementOnly
                                })

            else:
                # need to check here if user selected only country or also a state, if country show overview, if state show state related graphs
                location_list = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
                                'Newfoundland and Labrador', 'Northwest Territories', 'Nova Scotia', 'Nunavut',
                                'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']
                
     return render(request, 'pdfgenerator.html',
                    {'state': final_state_list, 'perc': final_mean_perc_list, 'form': form, 'st': s, 'ex': exp,
                    'mydata': data, 'firststat': numberofdistricts, 'secondstat': numberofstates,
                    'thirdstat': numberofproducts, 'products': products, 'suburb': suburb, 'rural': rural, 'town': town,
                    'city': city, 'localtype': type_of_local, 'pro': productsOnly, 'engo': engagementOnly,
                    'stb': states_for_broadband,
                    'avgb': average_for_broadband, 'engagement': engagement, 'product_info': product_info, 'time': time,
                    'reduced_free': multiple_reduced_values, "pct_free": multiple_pct_ethic,
                    'multiple_state': multiple_state, 'lepro': leastProductsOnly, 'leeng': leastEngagementOnly
                    })


def generate_data_for_online_activities_by_gender_from_stats_canada():
    # This method should be invoked only when there is a change to this table for today's date.
    df = stats_can.sc.zip_table_to_dataframe('2210013701')
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = (df[(df.Gender == 'Total, gender') & (
            (df.COORDINATE == '1.1.1.1.1') | (df.COORDINATE == '1.2.1.1.1') | (df.COORDINATE == '1.3.1.1.1') | (
            df.COORDINATE == '1.4.1.1.1') | (df.COORDINATE == '1.5.1.1.1') | (df.COORDINATE == '1.6.1.1.1') | (
                    df.COORDINATE == '1.13.1.1.1') | (df.COORDINATE == '1.12.1.1.1') | (
                    df.COORDINATE == '1.23.1.1.1') | (df.COORDINATE == '1.26.1.1.1') | (
                    df.COORDINATE == '1.28.1.1.1'))])
    print(df.columns)
    df = df[['REF_DATE', 'Online_activities', 'Gender', 'Age_group', 'VALUE']]
    print(df)

    print(is_stats_canada_table_updated(2210013701))

# heat map
def labour_force_data():
    labour_status = LabourForce.objects.all()
    print("The labour status")
    labour_dict = {}
    for item in labour_status:
        if item.reference_date not in labour_dict.keys():
            labour_dict[item.reference_date] = {}
        else:
            labour_dict[item.reference_date][item.labour_force_status] = item.value

    return labour_dict

# line graph
def post_enrollment_data():
    enrollment_data = PostSecondaryEnrollment.objects.all()
    print("The postsecondary status")
    enrollment_dict = {}
    for item in enrollment_data:
        if item.reference_date not in enrollment_dict.keys():
            enrollment_dict[item.reference_date] = {}
        elif item.institution_type == "Total, institution type":
            enrollment_dict[item.reference_date][item.geo] = item.value
        else:
            pass

    return enrollment_dict


# sychronized chart

def expenditure_college_data():
    expenditure_data = ExpenditureColleges.objects.all()
    print("The expenditure status")
    expenditure_dict = {}
    for item in expenditure_data:
        if item.reference_date not in expenditure_dict.keys():
            expenditure_dict[item.reference_date] = {}
        elif item.geo not in expenditure_dict[item.reference_date].keys():
            expenditure_dict[item.reference_date][item.geo] = []
        else:
            expenditure_dict[item.reference_date][item.geo].append(item.value)
    return expenditure_dict
    print("the value is",expenditure_dict)

# bar graph
def apprentice_registration_data():
    apprentice_data = ApprenticeshipRegistration.objects.all()
    print("The apprentice status")
    apprentice_dict = {}
    for item in apprentice_data:
        if item.reference_date not in apprentice_dict.keys():
            apprentice_dict[item.reference_date] = {}
        elif apprentice_data.trade_groups == "Total major trade groups":
            apprentice_dict[item.reference_date][item.geo] = item.value
        else:
            pass

    print("the value is",apprentice_dict)
#  multi bar graph
def avg_test_score_data():
    test_score_data = AverageTestScores.objects.all()
    print("The test score status")
    test_score_dict = {}
    for item in test_score_data:
        if item.reference_date not in test_score_dict.keys():
            test_score_dict[item.reference_date] = {}
        elif item.gender not in test_score_dict[item.reference_date].keys():
            test_score_dict[item.reference_date][item.gender] = []
        elif item.characteristics == "Estimated average score":
            test_score_dict[item.reference_date][gender].append(item.value)
        else:
            pass

    print("the value is",apprentice_dict)

# speedometer
def participation_rate_data():
    participation_data = ParticipationRate.objects.all()
    print("The test score status")
    participation_dict = {}
    for item in participation_data:
        if item.reference_date not in test_score_dict.keys():
            participation_dict[item.reference_date] = {}
        elif item.age not in participation_dict[item.reference_date].keys():
            participation_dict[item.reference_date][item.age] = []
        else:
            participation_dict[item.reference_date][item.age].append(item.value)

    print("the value is",apprentice_dict)

#
def unemployment_rate_data():
    unemployment_data = UnemploymentRate.objects.all()
    print("The test score status")
    unemployment_dict = {}
    for item in unemployment_data:
        if item.reference_date not in test_score_dict.keys():
            unemployment_dict[item.reference_date] = {}
        elif item.age not in unemployment_dict [item.reference_date].keys():
            unemployment_dict[item.reference_date][item.characteristics_of_the_population] = []
        else:
            unemployment_dict[item.reference_date][item.characteristics_of_the_population].append(item.value)

    print("the value is",apprentice_dict)






def is_stats_canada_table_updated(productId):
    # The logic to check if a table with a product id is updated, if it is updated then call the associated table methods to make a call to statscan api.
    updated_tables_today_dict = (StatsCan.tables_updated_today())

    for x in updated_tables_today_dict:
        for key in x.keys():
            if key == 'productId' and x[key] == productId:
                return "Updated Today"

    return "Not Updated Today"


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

    return county_connection, district_list


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
    states = ['Utah', 'Illinois', 'Wisconsin', 'North Carolina', 'Missouri', 'Washington', 'New York', 'Indiana',
              'Virginia', 'New Jersey', 'Texas']

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
        elif item.state == 'New York':
            newyork.append(item.pp_total_raw)
        elif item.state == 'Indiana':
            indiana.append(item.pp_total_raw)
        elif item.state == 'Virginia':
            vir.append(item.pp_total_raw)
        elif item.state == 'New Jersey':
            jersey.append(item.pp_total_raw)
            dis.append(item.pp_total_raw)
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
    if len(jersey) > 0:
        avg_expenditure_for_states.append(avg(jersey))
    else:
        avg_expenditure_for_states.append(0)
    if len(tex) > 0:
        avg_expenditure_for_states.append(avg(tex))
    else:
        avg_expenditure_for_states.append(0)

    return states, avg_expenditure_for_states


def productEngagement():
    obj = EngagementInfo.objects.all().order_by('-engagement_index')

    products = ProductsInfo.objects.all()
    products_data = []
    consumer_products = []
    products_array = []
    single_products_array = []
    single_average_engagement_array = []
    products_with_least_engagement_array = []
    least_engagement_array = []

    for x in obj:
        for product in products:
            if x.lp_id == product.lpid:
                products_data.append({'name': product.product_name, 'engagement': x.engagement_index})

    for dic in products_data:
        for key in (dic.keys()):
            if key == 'name':
                consumer_products.append(dic[key])
    unique_products = set(consumer_products)

    for p in unique_products:
        average = 0
        count = 0
        for dict in products_data:
            if dict['name'] == p:
                average = average + dict['engagement']
                count = count + 1
        products_array.append({'name': p, 'avg': average / count})

    top10products = sorted(products_array, key=itemgetter('avg'), reverse=True)[0:10]

    least10products = sorted(products_array, key=itemgetter('avg'), reverse=True)[-15:-5]

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
        product_data.append({"product_name": product.product_name, "url": product.url})

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
        free_reduce[state] = round(np.mean(free_reduce[state]), 2)
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
        # print(p_info)

    return engagement, time, p_info


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
    # print("The states", states)

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
    return (int(j / len(li)))


@login_required(login_url='/dashboard/accounts/login/')
def show_graphs_for_users(request):
    # userObject = UserProfile.objects.filter(user_id=request.user.id)
    logged_in_user_type = request.user.userprofile.user_type
    # print('Logged in user type is',logged_in_user_type )
    # print('This statement is',logged_in_user_type == 'student')
    if (logged_in_user_type == 'student'):
        return HttpResponseRedirect('/dashboard/student/')
    elif (logged_in_user_type == 'educator'):
        # call educator methods here
        # print('Hi educator')
        return HttpResponseRedirect('/dashboard/speedtest/')

    # forces user to login if they try to go /dashboard/home path


def canadian_data(request):
   # labour
   labour_dic = labour_force_data()
   labour_key = list(labour_dic["2018/2019"].keys())
   labour_value = list(labour_dic["2018/2019"].values())
   labour_key = json.dumps(labour_key)
   labour_value = json.dumps(labour_value)
   # enrollment
   enrollment_dic = post_enrollment_data()
   enrollment_key = list(enrollment_dic["2018/2019"].keys())
   enrollment_value = list(enrollment_dic["2018/2019"].values())
   enrollment_key = json.dumps(enrollment_key)
   enrollment_value = json.dumps(enrollment_value)
   # expenditure
   expenditure = expenditure_college_data()
   expenditure_key = ['Salaries and wages',
                      'Teachers',
                      'Other salaries and wages',
                      'Fringe benefits',
                      'Library acquisitions',
                      'Operational supplies and expenses',
                      'Utilities',
                      'Furniture and equipment',
                      'Scholarships and other related students support',
                      'Fees and contracted services',
                      'Debt services',
                      'Buildings',
                      'Land and site services',
                      'Miscellaneous',
                      'Ancillary enterprises']
   expenditure_value = list(expenditure['2018/2019']['Canada'][1:])
   expenditure_key = json.dumps(expenditure_key)
   expenditure_value = json.dumps(expenditure_value)

   return labour_key, labour_value, enrollment_key, enrollment_value, expenditure_key, expenditure_value


def mean_percentage_access_of_black_hispanic(request):
    # covidviews.covid_summary()
    # covidviews.all_sub_regions("ON")
    covidviews.single_health_region_info('3561')
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

    mean_perc.append(round((sum(Utah)) / len(Utah), 2))
    mean_perc.append(round((sum(Illi)) / len(Illi), 2))
    mean_perc.append(round((sum(Wisco)) / len(Wisco), 2))
    mean_perc.append(round((sum(north)) / len(north), 2))
    mean_perc.append(round((sum(miss)) / len(miss), 2))
    mean_perc.append(round((sum(wash)) / len(wash), 2))
    mean_perc.append(round((sum(newyork)) / len(newyork), 2))
    mean_perc.append(round((sum(indiana)) / len(indiana), 2))
    mean_perc.append(round((sum(vir)) / len(vir), 2))
    mean_perc.append(round((sum(jersey)) / len(jersey), 2))
    mean_perc.append(round((sum(tex)) / len(tex), 2))

    return states, mean_perc


@login_required(login_url='/dashboard/accounts/login/')
def percentage_access_black_hispanic(request):
    covidviews.covid_statistics_by_province_for_each_day('on', '2022')
    location_list = ['Utah', 'Illinois', 'Wisconsin', 'North Carolina', 'Missouri', 'Washington',
                                 'Massachusetts', 'New York', 'Indiana',
                                 'Virginia', 'New Jersey', 'Texas', 'District of Columbia']
    input_country = 'usa'
    labour_dic = {}
    labour_key = []
    labour_value = []
    enrollment_dic = {}
    enrollment_key = []
    enrollment_value = []
    expenditure_key = []
    expenditure_value = []
    expenditure = {}
    search = ''
    states,mean_perc = mean_percentage_access_of_black_hispanic(request)
    final_state_list = json.dumps(states)
    final_mean_perc_list = json.dumps(mean_perc)

    s, exp = expenditure_per_pupil_in_different_states()
    form = create_district_graph()
    county, district = percentage_access_in_state("Illinois")

    keyVal = {};
    originalData = []  # Data contains array of objects

    i = 0
    for i in range(len(s)):
        originalData.append({"state": s[i], "expenditure": exp[i]});

    data = json.dumps(originalData)  # data in JSON format ready to be used by d3.js

    numberofdistricts, numberofstates = totalNumberOfSchoolDistricts()  # statistic 1
    
    products, numberofproducts = total_number_of_products()  # statistic 2

    suburb, rural, town, city, type_of_local = total_locale_type()

    bottomProducts, engagementOfLeastProducts, productsOnly, engagementOnly = productEngagement()

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
            # print(":", y)
            reduced_values.remove(y)
            reduced_keys.remove(x)

    multiple_reduced_values = json.dumps(reduced_values[:len(mean_perc)])
    multiple_pct_ethic = json.dumps(mean_perc[:len(mean_perc)])
    multiple_state = json.dumps(reduced_keys[:len(mean_perc)])

    context = {'state': final_state_list, 'perc': final_mean_perc_list, 'form': form, 'st': s, 'ex': exp,
                    'mydata': data, 'firststat': numberofdistricts, 'secondstat': numberofstates,
                    'thirdstat': numberofproducts, 'products': products, 'suburb': suburb, 'rural': rural, 'town': town,
                    'city': city, 'localtype': type_of_local, 'pro': productsOnly, 'engo': engagementOnly,
                    'stb': states_for_broadband,
                    'avgb': average_for_broadband, 'engagement': engagement, 'product_info': product_info, 'time': time,
                    'reduced_free': multiple_reduced_values, "pct_free": multiple_pct_ethic,
                    'multiple_state': multiple_state, 'lepro': leastProductsOnly, 'leeng': leastEngagementOnly,'inputcountry':input_country, 'location_list': location_list
                }
    template = 'index.html'

    if request.method == 'POST':
        
        form = FilterForm(request.POST)
        if form.is_valid():

            input_country = request.POST.get('country')
            input_location = ''
            if (request.POST.get('locations') != None):
                input_location = request.POST.get('locations')

            if input_country == 'usa':
                location_list = ['Utah', 'Illinois', 'Wisconsin', 'North Carolina', 'Missouri', 'Washington',
                                 'Massachusetts', 'New York', 'Indiana',
                                 'Virginia', 'New Jersey', 'Texas', 'District of Columbia']
                if input_location in location_list:
                    # state related data
                    template = 'state.html'
                

                else:
                    print("WE are in USA SECTION 1.0")
                    template = 'index.html'
                    context = {'state': final_state_list, 'perc': final_mean_perc_list, 'form': form, 'st': s, 'ex': exp,
                    'mydata': data, 'firststat': numberofdistricts, 'secondstat': numberofstates,
                    'thirdstat': numberofproducts, 'products': products, 'suburb': suburb, 'rural': rural, 'town': town,
                    'city': city, 'localtype': type_of_local, 'pro': productsOnly, 'engo': engagementOnly,
                    'stb': states_for_broadband,
                    'avgb': average_for_broadband, 'engagement': engagement, 'product_info': product_info, 'time': time,
                    'reduced_free': multiple_reduced_values, "pct_free": multiple_pct_ethic,
                    'multiple_state': multiple_state, 'lepro': leastProductsOnly, 'leeng': leastEngagementOnly, 'inputcountry':input_country, 'inputlocation': input_location, 'location_list': location_list
                    }
                   
            else:
                # need to check here if user selected only country or also a state, if country show overview, if state show state related graphs
                location_list = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
                                 'Newfoundland and Labrador', 'Northwest Territories', 'Nova Scotia', 'Nunavut',
                                 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']
                print("This is canada's section")
                labour_key,labour_value,enrollment_key,enrollment_value,expenditure_key,expenditure_value = canadian_data(request)
                print(labour_key)
                print(labour_value)
                template = 'index2.html'
                context = {
                    'labour_key': labour_key, 'labour_value': labour_value, 'enrollment_key': enrollment_key,
                    'enrollment_value': enrollment_value, 'expenditure_key': expenditure_key,
                    'expenditure_value': expenditure_value,'inputcountry':input_country, 'inputlocation': input_location, 'location_list': location_list
                }
        else:
            search = request.POST.get('searchbox')
            template = 'search.html'

            if search == "":
                template="index.html"
                context = {'state': final_state_list, 'perc': final_mean_perc_list, 'form': form, 'st': s, 'ex': exp,
                    'mydata': data, 'firststat': numberofdistricts, 'secondstat': numberofstates,
                    'thirdstat': numberofproducts, 'products': products, 'suburb': suburb, 'rural': rural, 'town': town,
                    'city': city, 'localtype': type_of_local, 'pro': productsOnly, 'engo': engagementOnly,
                    'stb': states_for_broadband,
                    'avgb': average_for_broadband, 'engagement': engagement, 'product_info': product_info, 'time': time,
                    'reduced_free': multiple_reduced_values, "pct_free": multiple_pct_ethic,
                    'multiple_state': multiple_state, 'lepro': leastProductsOnly, 'leeng': leastEngagementOnly, 'inputcountry':input_country, 'location_list': location_list
                    }
            else:
                context = search_feature(search)
                context['searchedword'] = search

                if(len(context) == 1):
                    context["nothingfound"] = "No search results found"
            
            
    return render(request, template, context)            
    
  
