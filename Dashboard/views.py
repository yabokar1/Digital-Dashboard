import math
from re import T
from typing import Protocol
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import json
import requests
import numpy as np
import pyspeedtest
# from .models import LabourForce
from bs4 import BeautifulSoup
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, ProfileForm
from .models import Districts, Students
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
from .models import FileUploadInfo
from .models import SpecialEducation
from .models import SchoolBoardAchievements
from .models import Hotspot
from .models import Tweets
from .view import covidviews
from .view import webscraper
from .view import canadianviews
from .view import kaggleviews
from .view import apiviews

from django.contrib.auth.decorators import login_required
from random import randint

import stats_can
from stats_can import StatsCan
from statistics import mean
from operator import itemgetter
import pickle
import csv
import pandas as pd
import ast
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import StudentSerializer,StudentSerializerWithToken
from django.contrib.auth.hashers import make_password


names_of_places = []
library_places = []
rating_star_list = []


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
 
    def validate(self,attrs):
        data = super().validate(attrs)
        student = Students.objects.all()
        serializer = StudentSerializerWithToken(student).data
        for k,v in serializer.items():
            data[k] = v

        return data

   
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    print("The token is",serializer_class.validate.__dict__)


@api_view(['GET'])
def getStudentProfile(request):
    student = Students.objects.all()
    serializer = StudentSerializerWithToken(student, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def registerStudent(request):
    data = request.data

    student = Students.objects.create(
        first_name = data['first'],
        last_name = data['last'],
        school = data['school'],
        grade = data['grade'],
        student_number = make_password(data['id'])
        
    )


@api_view(['POST'])
def getStudent(request):
    body = request.data
    print("The body has", body)
    print("Hello")
    first_name = body['first']
    student_id = body['id']
    print("The student has", first_name,student_id)
    student = Students.objects.filter(first_name=
    first_name,student_number=student_id)
    serializer = StudentSerializerWithToken(student, many=True)
    return Response(serializer.data)

    


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
    return render(request, 'speedtest.html')


def show_user_login__page(request):
    return render(request, 'login.html')


def show_join_us_page(request):
    return render(request, 'joinustoday.html')


def show_sign_up_page(request):
    return render(request, 'sign-up.html')

def mentalhealth(request):
    return render(request,"mentalhealth.html")

def show_interactive_dashboard_page(request):
    return render(request,"interactivevisuals.html")


def show_pdf_summary_extractor_page(request):
    pdf_summaries = []
    results_list = []
    search_keywords = ""
    error_message = ""
    search = 'digital+learning+ontario+public+schools'
    if request.method == 'POST' and request.POST.get('searchforpdf'):
        print("The term is ",request.POST.get('searchforpdf'))
        search = request.POST.get('searchforpdf')

        search_list = str(search).split(" ")
        for x in search_list:
            search_keywords+=x+"+"

        search = search_keywords[0:len(search_keywords)-1]
    # search = 'digital+learning+ontario+public+schools'

    results_list, db_data_found = canadianviews.pdf_finder_retriever(search)

    if len(results_list) == 0:
        error_message = 'Search results not found'
    else: 
        if len(results_list) >= 4:
            print("result values are greater than equal to 5")
            pdf_summaries = canadianviews.read_pdf(results_list[0:4], search, db_data_found)
        
        if len(results_list) == 1 or len(results_list) == 2 or len(results_list) == 3:
            print("result values are less than equal to 3")
            pdf_summaries = canadianviews.read_pdf(results_list, search, db_data_found)

    return render(request,"pdfsummaryextractor.html", context={'pdfsummaries': pdf_summaries, 'error': error_message})


def show_file_upload_csv_page(request):
    csv_dict = {}
    context = {}
    username = ''
    columns = []
    pickled_object = []
    csv_file = ""
    vertical_bar = ""
    horizontal_bar = ""
    invalid = ""
    if request.method == 'POST' and request.POST.get('xcolumn') and request.POST.get('ycolumn'):
        xcol = request.POST.get('xcolumn')
        ycol = request.POST.get('ycolumn')
        fname = request.POST.get('filename')
        graph_type = request.POST.get('graph')
        username = request.user
        x_list = []
        y_list = []
        print("The graph type is", graph_type)
        record = FileUploadInfo.objects.all()
        for x in record:
              
            if (x.file_name == fname and x.user_name == str(username)):
                pickled_object = x.pickle
        
        for x in pickled_object:
            for key, value in x.items():
                if key == xcol:
                  x_list.append(value)
                if key == ycol:
                    y_list.append(value)  
        
        if (graph_type == 'line'):
            if "Time" in xcol or "time" in xcol or "Months" in xcol or "months" in xcol or "Days" in xcol or "days" in xcol or "Year" in xcol or "year" in xcol:
                for y in y_list:
                    if type(y) == int or type(y) == float:
                        context['xdata'] = x_list
                        context['ydata'] = y_list
                        context['xlabel'] = xcol
                        context['ylabel'] = ycol
                        context['line_bar'] = "line"
                    else:
                        print("I am in error part of inner if statement")
                        context['errormessage'] = "Line graph is not supported"

            else:
                print("I am in error part of outer if statement")
                context['errormessage'] = "X axis for a line graph has to be time"

        elif (graph_type == 'bar'):

            for x in x_list:
                for y in y_list:
                    if (((type(x) == int or type(x) == float) and (type(y) == int or type(y) == float)) or ((type(x) == str or type(x) == str) and (type(y) == str or type(y) == str))):
                        invalid = "true"
                        context['errormessage'] = "Both column types cannot be same."

            
            if invalid != "true":
                for x in x_list:
                    if (type(x) == str and len(x) <= 12):
                        vertical_bar = "vbar"

                        context['xdata'] = x_list
                        context['ydata'] = y_list
                        context['xlabel'] = xcol
                        context['ylabel'] = ycol
                        context['vertical_bar'] = vertical_bar

                    elif type(x) == float or type(x) == int:
                        horizontal_bar = "hbar"

                        context['xdata'] = x_list
                        context['ydata'] = y_list
                        context['xlabel'] = xcol
                        context['ylabel'] = ycol
                        context['horizontal_bar'] = horizontal_bar
                    else:
                        context['errormessage'] = "X axis chosen is either not supported or the x axis values are too long in length."

                for y in y_list:
                    if(type(y) == int or type(y) == float):
                        vertical_bar = "vbar"
                        
                        context['xdata'] = x_list
                        context['ydata'] = y_list
                        context['xlabel'] = xcol
                        context['ylabel'] = ycol
                        context['vertical_bar'] = vertical_bar
                    
                    elif type(y) == str and len(y) <= 12:
                        horizontal_bar = "hbar"

                        context['xdata'] = x_list
                        context['ydata'] = y_list
                        context['xlabel'] = xcol
                        context['ylabel'] = ycol
                        context['horizontal_bar'] = horizontal_bar

                    else:
                        context['errormessage'] = "Y axis chosen is either not supported or the Y axis values are too long in length."

  
        print("The context is", context)

    elif request.method == 'POST' and len(request.FILES) != 0 and request.FILES['file'].name.endswith('csv'):
        try:
            csv_file = request.FILES['file']
            print("The file is",csv_file)
            file_size =  csv_file.size
            if (file_size <= 5000000):
                df = pd.read_csv(csv_file)
                csv_dict = (df.to_dict('records'))
                
                username = request.user
                print("The bous username is", username)
                if not FileUploadInfo.objects.filter(pickle=csv_dict, user_name=username).exists():
                    FileUploadInfo.objects.create(file_name=csv_file, pickle=csv_dict, user_name=username)

                record = FileUploadInfo.objects.all()
                for x in record:
                    if (x.file_name == str(csv_file) and x.user_name == str(username)):
                        pickled_object = x.pickle

                for x in pickled_object:
                    for k in x.keys():
                        if k not in columns:
                            columns.append(k)
                print("The columns are", columns)
                context['col'] = columns
                context['fname'] = csv_file

            else:
                context['errormessage'] = "The file size can be maximum of 5 MB."
        except:
            context['errormessage'] = "An error occured, please make sure that csv file imported is in correct format."
        


    elif request.method == 'POST' and len(request.FILES) != 0 and not request.FILES['file'].name.endswith('csv'):
        context['errormessage'] = "this is not a csv"

        
    return render(request, 'fileupload.html', context)

def convert_to_bytes_using_pickle(obj):
    # dict = {'name': 'Qasim', 'income': 1000, 'age': 25}
    pickled_object = (pickle.dumps(obj))
    return pickled_object

def convert_from_bytes_to_object(bytes):
    object = pickle.loads(bytes)
    return object
    

def search_tweets(item):
    search_words = ('Internet', 'Device', 'Mental Health', 'Performance')
    tweets = []
    tweet_list = []
    if (item in search_words):
        tweets = Tweets.objects.filter(category=item)
    for tweet in tweets:
        tweet_list.append({'text': item.text, 'category': item.category,  'retweets': item.retweets, 'likes':item.likes, "date": item.date})


            

def search_feature(word):
    search_words = ('engagement', 'expenditure', 'product', 'school', 'schools', 'access', 'districts', 'broadband', 'internet', 'black', 'hispanic')
    context = {}
    context.clear()

    if (word in search_words):
        if (word == 'expenditure'):
            states, expenditure = kaggleviews.expenditure_per_pupil_in_different_states()
            context['states'] = states
            context['exp'] = expenditure
        if word == 'engagement' or word == 'product':
            bottomProducts, engagementOfLeastProducts, productsOnly, engagementOnly = kaggleviews.productEngagement()
            
            context['highengproducts'] = productsOnly
            context['higheng'] = engagementOnly
            context['lowengproducts'] = bottomProducts
            context['loweng'] = engagementOfLeastProducts

        if word == 'product':
            products, numberofproducts = kaggleviews.total_number_of_products()
            
            context['namesofproducts'] = products
            context['learningproductcount'] = numberofproducts

        if word == 'broadband' or word == 'internet':
            st, broadband_average = kaggleviews.broadband_connection()
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

     s, exp = kaggleviews.expenditure_per_pupil_in_different_states()
    # print("Expenditure is",exp)
     form = kaggleviews.create_district_graph()
     county, district = kaggleviews.percentage_access_in_state("Illinois")

     keyVal = {};
     originalData = []  # Data contains array of objects

     i = 0
     for i in range(len(s)):
        originalData.append({"state": s[i], "expenditure": exp[i]});

     data = json.dumps(originalData)  # data in JSON format ready to be used by d3.js

     numberofdistricts, numberofstates = kaggleviews.totalNumberOfSchoolDistricts()  # statistic 1
    # print('Total number of districts is', numberofdistricts)

     products, numberofproducts = kaggleviews.total_number_of_products()  # statistic 2

     suburb, rural, town, city, type_of_local = kaggleviews.total_locale_type()

     bottomProducts, engagementOfLeastProducts, productsOnly, engagementOnly = kaggleviews.productEngagement()

     productsOnly = json.dumps(productsOnly)
     engagementOnly = json.dumps(engagementOnly)
     leastProductsOnly = json.dumps(bottomProducts)
     leastEngagementOnly = json.dumps(engagementOfLeastProducts)

     st, broadband_average = kaggleviews.broadband_connection()
     states_for_broadband = json.dumps(st)
     average_for_broadband = json.dumps(broadband_average)

     engagement, time, product_info = kaggleviews.product_engage(60825)
     engagement = json.dumps(engagement)
     time = json.dumps(time)
     product_info = json.dumps(product_info)

     reduced = kaggleviews.free_reduced()

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



def generate_product_info(request):
    return render(request, 'main.html')


@login_required(login_url='/dashboard/accounts/login/')
def show_graphs_for_users(request):
    # userObject = UserProfile.objects.filter(user_id=request.user.id)
    logged_in_user_type = request.user.userprofile.user_type
    # print('Logged in user type is',logged_in_user_type )
    # print('This statement is',logged_in_user_type == 'student')
    if (logged_in_user_type == 'student'):
        return HttpResponseRedirect('/dashboard/students/')
    elif (logged_in_user_type == 'policymaker'):
        # call educator methods here
        # print('Hi educator')
        return HttpResponseRedirect('/dashboard/researcher/')

    # forces user to login if they try to go /dashboard/home path


def canadian_data(request, date, identifier):
#    webscraper.webscraperfordataontario()
   # labour 

    if (identifier == ''):
        labour_dic = canadianviews.labour_force_data()
        labour_key = list(labour_dic["2018/2019"].keys())
        labour_value = list(labour_dic["2018/2019"].values())
        labour_key = json.dumps(labour_key)
        labour_value = json.dumps(labour_value)
        # enrollment
        enrollment_dic = canadianviews.post_enrollment_data()
        enrollment_key = list(enrollment_dic["2019/2020"].keys())
        enrollment_value = list(enrollment_dic["2019/2020"].values())
        enrollment_key = json.dumps(enrollment_key)
        enrollment_value = json.dumps(enrollment_value)
        # expenditure
        expenditure = canadianviews.expenditure_college_data()
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
        
        expenditure_value = list(expenditure['2019/2020']['Canada'][1:])
        
        expenditure_key = json.dumps(expenditure_key)
        expenditure_value = json.dumps(expenditure_value)

        #Aprenticeship
        apprentice_dict = canadianviews.apprentice_registration_data()
        apprentice_keys = []
        apprentice_keys = list(apprentice_dict['2020-01-01 00:00:00'].keys())
        apprentice_values = list(apprentice_dict['2020-01-01 00:00:00'].values())
        
        # Test scores
        test_dict = canadianviews.avg_test_score_data()
        test_scores_males_values = []
        test_scores_females_values = []

        test_scores_keys = ['Reading', 'Mathematics', 'Science']
        test_scores_males_values.append(mean(list(test_dict['2018-01-01 00:00:00']['Male gender']['Reading'])))
        test_scores_males_values.append(mean(list(test_dict['2018-01-01 00:00:00']['Male gender']['Science'])))
        test_scores_males_values.append(mean(list(test_dict['2018-01-01 00:00:00']['Male gender']['Mathematics'])))
        
        test_scores_females_values.append(mean(list(test_dict['2018-01-01 00:00:00']['Female gender']['Reading'])))
        test_scores_females_values.append(mean(list(test_dict['2018-01-01 00:00:00']['Female gender']['Science'])))
        test_scores_females_values.append(mean(list(test_dict['2018-01-01 00:00:00']['Female gender']['Mathematics'])))
        

        #participation
        participation_dict = canadianviews.participation_rate_data()
        participation_keys = []
        participation_values = []
        for key,value in participation_dict['2020/2021'].items():
            participation_keys.append(key)
            participation_values.append(int(round(mean(value), 2)))


        #unemployment
        unemployment_dict = canadianviews.unemployment_rate_data()
        unemployment_keys = list(unemployment_dict['2018-01-01 00:00:00'].keys())
        unemployment_values = []

        for key, value in unemployment_dict['2018-01-01 00:00:00'].items():
            unemployment_values.append(round(mean(value), 2))

            
            #special education
        exceptionality_list, elementary_list, secondary_list, total_list = webscraper.special_education_data()

        #board achievements
        board_list, grade_ten_osslt_list, grade_six_eqao_list, four_year_grad_list = webscraper.school_board_achievements_data()
    
    else:
        labour_dic = canadianviews.labour_force_data()
        labour_key = list(labour_dic["2018/2019"].keys())
        labour_value = list(labour_dic["2018/2019"].values())
        labour_key = json.dumps(labour_key)
        labour_value = json.dumps(labour_value)
        # enrollment
        enrollment_dic = canadianviews.post_enrollment_data()
        enrollment_key = list(enrollment_dic["2019/2020"].keys())
        enrollment_value = list(enrollment_dic["2019/2020"].values())
        enrollment_key = json.dumps(enrollment_key)
        enrollment_value = json.dumps(enrollment_value)
        # expenditure
        expenditure = canadianviews.expenditure_college_data()
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
        
        expenditure_value = list(expenditure['2019/2020']['Canada'][1:])
        
        expenditure_key = json.dumps(expenditure_key)
        expenditure_value = json.dumps(expenditure_value)

        #Aprenticeship
        apprentice_dict = canadianviews.apprentice_registration_data()
        apprentice_keys = []
        apprentice_keys = list(apprentice_dict['2020-01-01 00:00:00'].keys())
        apprentice_values = list(apprentice_dict['2020-01-01 00:00:00'].values())
        
        # Test scores
        test_dict = canadianviews.avg_test_score_data()
        test_scores_males_values = []
        test_scores_females_values = []

        if identifier == 'testscoresdate':
            test_scores_keys = ['Reading', 'Mathematics', 'Science']
            test_scores_males_values.append(mean(list(test_dict[date]['Male gender']['Reading'])))
            test_scores_males_values.append(mean(list(test_dict[date]['Male gender']['Science'])))
            test_scores_males_values.append(mean(list(test_dict[date]['Male gender']['Mathematics'])))
            
            test_scores_females_values.append(mean(list(test_dict[date]['Female gender']['Reading'])))
            test_scores_females_values.append(mean(list(test_dict[date]['Female gender']['Science'])))
            test_scores_females_values.append(mean(list(test_dict[date]['Female gender']['Mathematics'])))

        # test_scores_keys = ['Reading', 'Mathematics', 'Science']
        # test_scores_males_values.append(mean(list(test_dict['2018-01-01 00:00:00']['Male gender']['Reading'])))
        # test_scores_males_values.append(mean(list(test_dict['2018-01-01 00:00:00']['Male gender']['Science'])))
        # test_scores_males_values.append(mean(list(test_dict['2018-01-01 00:00:00']['Male gender']['Mathematics'])))
        
        # test_scores_females_values.append(mean(list(test_dict['2018-01-01 00:00:00']['Female gender']['Reading'])))
        # test_scores_females_values.append(mean(list(test_dict['2018-01-01 00:00:00']['Female gender']['Science'])))
        # test_scores_females_values.append(mean(list(test_dict['2018-01-01 00:00:00']['Female gender']['Mathematics'])))
        

        #participation
        participation_dict = canadianviews.participation_rate_data()
        participation_keys = []
        participation_values = []
        for key,value in participation_dict['2020/2021'].items():
            participation_keys.append(key)
            participation_values.append(int(round(mean(value), 2)))


        #unemployment
        unemployment_dict = canadianviews.unemployment_rate_data()
        unemployment_keys = list(unemployment_dict['2018-01-01 00:00:00'].keys())
        unemployment_values = []

        for key, value in unemployment_dict['2018-01-01 00:00:00'].items():
            unemployment_values.append(round(mean(value), 2))

            
            #special education
        exceptionality_list, elementary_list, secondary_list, total_list = webscraper.special_education_data()

        #board achievements
        board_list, grade_ten_osslt_list, grade_six_eqao_list, four_year_grad_list = webscraper.school_board_achievements_data()
        
      

    return labour_key, labour_value, enrollment_key, enrollment_value, expenditure_key, expenditure_value,apprentice_keys, apprentice_values,test_scores_keys, test_scores_males_values, test_scores_females_values,participation_keys, participation_values,unemployment_keys, unemployment_values, exceptionality_list, elementary_list, secondary_list, total_list, board_list, grade_ten_osslt_list, grade_six_eqao_list, four_year_grad_list    



@login_required(login_url='/dashboard/accounts/login/')
def views_for_researcher(request):
    # generate_data_for_online_activities_by_gender_from_stats_canada()
    # pdf_list = canadianviews.pdf_finder()
    # canadianviews.read_pdf(pdf_list)


    # search = 'digital+learning+ontario+public+schools'
    # results_list, db_data_found = canadianviews.pdf_finder_retriever(search)

    # if len(results_list) == 0:
    #     print('Search results not found')
    # else: 
    #     if len(results_list) >= 4:
    #         print("result values are greater than equal to 5")
    #         canadianviews.read_pdf(results_list[0:4], search, db_data_found)
        
    #     if len(results_list) == 1 or len(results_list) == 2 or len(results_list) == 3:
    #         print("result values are less than equal to 3")
    #         canadianviews.read_pdf(results_list, search, db_data_found)

    
    
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
    exceptionality_keys = []
    elementary_values = []
    secondary_values = []
    total_values = []
    board_keys = []
    grade_ten_osslt_values = []
    grade_six_eqao_values = []
    four_year_grad_values = []
    states,mean_perc = kaggleviews.mean_percentage_access_of_black_hispanic(request)
    final_state_list = json.dumps(states)
    final_mean_perc_list = json.dumps(mean_perc)

    s, exp = kaggleviews.expenditure_per_pupil_in_different_states()
    form = kaggleviews.create_district_graph()

    # not being used
    # county, district = percentage_access_in_state("Illinois")

    keyVal = {};
    originalData = []  # Data contains array of objects

    i = 0
    for i in range(len(s)):
        originalData.append({"state": s[i], "expenditure": exp[i]});

    data = json.dumps(originalData)  # data in JSON format ready to be used by d3.js

    numberofdistricts, numberofstates = kaggleviews.totalNumberOfSchoolDistricts()  # statistic 1
    
    products, numberofproducts = kaggleviews.total_number_of_products()  # statistic 2

    suburb, rural, town, city, type_of_local = kaggleviews.total_locale_type()

    bottomProducts, engagementOfLeastProducts, productsOnly, engagementOnly = kaggleviews.productEngagement()

    productsOnly = json.dumps(productsOnly)
    engagementOnly = json.dumps(engagementOnly)
    leastProductsOnly = json.dumps(bottomProducts)
    leastEngagementOnly = json.dumps(engagementOfLeastProducts)

    st, broadband_average = kaggleviews.broadband_connection()
    states_for_broadband = json.dumps(st)
    average_for_broadband = json.dumps(broadband_average)

    engagement, time, product_info = kaggleviews.product_engage(60825)
    engagement = json.dumps(engagement)
    time = json.dumps(time)
    product_info = json.dumps(product_info)

    reduced = kaggleviews.free_reduced()

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
    template = 'americandataforresearcher.html'

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
                    # template = 'state.html'
                    print("state.html for canada still needs to be figured")
                

                else:
                    template = 'americandataforresearcher.html'
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
                print("My location is", input_location)
                if input_location == "":
                    # need to check here if user selected only country or also a state, if country show overview, if state show state related graphs
                    location_list = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
                                    'Newfoundland and Labrador', 'Northwest Territories', 'Nova Scotia', 'Nunavut',
                                    'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']
                    labour_key,labour_value,enrollment_key,enrollment_value,expenditure_key,expenditure_value, apprentice_keys, apprrentice_values, test_score_keys, test_score_males_values, test_score_female_values, participation_keys, participation_values, unemployment_keys, unemployemnt_values, exceptionality_keys, elementary_values, secondary_values, total_values, board_keys, grade_ten_osslt_values, grade_six_eqao_values, four_year_grad_values = canadian_data(request, 'date', '')
                    
                    template = 'canadiandataforresearcher.html'
                    context = {
                        'labour_key': labour_key, 'labour_value': labour_value, 'enrollment_key': enrollment_key,
                        'enrollment_value': enrollment_value, 'expenditure_key': expenditure_key,
                        'expenditure_value': expenditure_value,'inputcountry':input_country, 'inputlocation': input_location, 'location_list': location_list, 'apprenticekeys': apprentice_keys, 'apprenticevalues': apprrentice_values, 'testscorekeys': test_score_keys, 'testscoremalesvalues': test_score_males_values, 'testscorefemalesvalues': test_score_female_values, 'participationratekeys': participation_keys, 'participationvalues': participation_values, 'unemploymentkeys': unemployment_keys, 'unemploymentvalues': unemployemnt_values 
                    }
                else:
                    template = 'provincesdata.html'
                    labour_key,labour_value,enrollment_key,enrollment_value,expenditure_key,expenditure_value, apprentice_keys, apprrentice_values, test_score_keys, test_score_males_values, test_score_female_values, participation_keys, participation_values, unemployment_keys, unemployemnt_values, exceptionality_keys, elementary_values, secondary_values, total_values, board_keys, grade_ten_osslt_values, grade_six_eqao_values, four_year_grad_values = canadian_data(request, '', '')
                    context = {
                        'labour_key': labour_key, 'labour_value': labour_value, 'enrollment_key': enrollment_key,
                        'enrollment_value': enrollment_value, 'expenditure_key': expenditure_key,
                        'expenditure_value': expenditure_value,'inputcountry':input_country, 'inputlocation': input_location, 'location_list': location_list, 'exceptionalitykeys': exceptionality_keys, 'elementaryvalues': elementary_values, 'secondaryvalues': secondary_values, 'totalvalues': total_values, 'boardkeys': board_keys, 'gradetenossltvalues': grade_ten_osslt_values, 'gradesixeqaovalues': grade_six_eqao_values, 'fouryeargradvalues': four_year_grad_values
                    }
        # Filtering in graph level is only for canada, once we want to add filter for more graphs just make the elif condition for all html filter tag names. Use if statements to see which one user selected and pass on the date value to canadian data accordingly.
        elif request.POST.get('testscoresdate'):
            input_country = 'canada'
            input_location = request.POST.get('locations')
            location_list = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
                                    'Newfoundland and Labrador', 'Northwest Territories', 'Nova Scotia', 'Nunavut',
                                    'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']
            if request.POST.get('testscoresdate'):
                dateforaveragetestscores = request.POST.get('testscoresdate')
                identifier = 'testscoresdate'
                labour_key,labour_value,enrollment_key,enrollment_value,expenditure_key,expenditure_value, apprentice_keys, apprrentice_values, test_score_keys, test_score_males_values, test_score_female_values, participation_keys, participation_values, unemployment_keys, unemployemnt_values, exceptionality_keys, elementary_values, secondary_values, total_values, board_keys, grade_ten_osslt_values, grade_six_eqao_values, four_year_grad_values = canadian_data(request, dateforaveragetestscores, identifier)
            template = 'canadiandataforresearcher.html'
            context = {
                'labour_key': labour_key, 'labour_value': labour_value, 'enrollment_key': enrollment_key,
                'enrollment_value': enrollment_value, 'expenditure_key': expenditure_key,
                'expenditure_value': expenditure_value,'inputcountry':input_country, 'inputlocation': input_location, 'location_list': location_list, 'apprenticekeys': apprentice_keys, 'apprenticevalues': apprrentice_values, 'testscorekeys': test_score_keys, 'testscoremalesvalues': test_score_males_values, 'testscorefemalesvalues': test_score_female_values, 'participationratekeys': participation_keys, 'participationvalues': participation_values, 'unemploymentkeys': unemployment_keys, 'unemploymentvalues': unemployemnt_values, 'avgtestscoredate':dateforaveragetestscores  
            }
        else:
            search = request.POST.get('searchbox')
            template = 'search.html'

            if search == "":
                template="americandataforresearcher.html"
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


@login_required(login_url='/dashboard/accounts/login/')
def percentage_access_black_hispanic(request):
    # covidviews.covid_statistics_by_province_for_each_day('on', '2022')
    
    
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
    states,mean_perc = kaggleviews.mean_percentage_access_of_black_hispanic(request)
    final_state_list = json.dumps(states)
    final_mean_perc_list = json.dumps(mean_perc)

    s, exp = kaggleviews.expenditure_per_pupil_in_different_states()
    form = kaggleviews.create_district_graph()
    county, district = kaggleviews.percentage_access_in_state("Illinois")

    keyVal = {};
    originalData = []  # Data contains array of objects

    i = 0
    for i in range(len(s)):
        originalData.append({"state": s[i], "expenditure": exp[i]});

    data = json.dumps(originalData)  # data in JSON format ready to be used by d3.js

    numberofdistricts, numberofstates = kaggleviews.totalNumberOfSchoolDistricts()  # statistic 1
    
    products, numberofproducts = kaggleviews.total_number_of_products()  # statistic 2

    suburb, rural, town, city, type_of_local = kaggleviews.total_locale_type()

    bottomProducts, engagementOfLeastProducts, productsOnly, engagementOnly = kaggleviews.productEngagement()

    productsOnly = json.dumps(productsOnly)
    engagementOnly = json.dumps(engagementOnly)
    leastProductsOnly = json.dumps(bottomProducts)
    leastEngagementOnly = json.dumps(engagementOfLeastProducts)

    st, broadband_average = kaggleviews.broadband_connection()
    states_for_broadband = json.dumps(st)
    average_for_broadband = json.dumps(broadband_average)

    engagement, time, product_info = kaggleviews.product_engage(60825)
    engagement = json.dumps(engagement)
    time = json.dumps(time)
    product_info = json.dumps(product_info)

    reduced = kaggleviews.free_reduced()

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
                # labour_key,labour_value,enrollment_key,enrollment_value,expenditure_key,expenditure_value = canadian_data(request)
                
                template = 'index2.html'
                # context = {
                #     'labour_key': labour_key, 'labour_value': labour_value, 'enrollment_key': enrollment_key,
                #     'enrollment_value': enrollment_value, 'expenditure_key': expenditure_key,
                #     'expenditure_value': expenditure_value,'inputcountry':input_country, 'inputlocation': input_location, 'location_list': location_list
                # }
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



@api_view(['GET'])
def participation_rate(request):
    data = {}
    participation_data = ParticipationRate.objects.all()
    participation_dict = {}
    for item in participation_data:
        if item.reference_date not in participation_dict.keys():
            participation_dict[item.reference_date] = {}
        elif item.age not in participation_dict[item.reference_date].keys():
            participation_dict[item.reference_date][item.age] = []
        else:
            participation_dict[item.reference_date][item.age].append(item.percentage)

    participation_keys = []
    participation_values = []
    for key,value in participation_dict['2020/2021'].items():
        participation_keys.append(key)
        participation_values.append(int(round(mean(value), 2)))

    data = {
        'keys': participation_keys,
        'values' : participation_values
    }
    
    return Response(data)
    

@api_view(['GET'])
def test_score(request):
    data = {}
    test_score_data = AverageTestScores.objects.all()
    test_score_dict = {}
    for item in test_score_data:
        if item.reference_date not in test_score_dict.keys():
            test_score_dict[item.reference_date] = {}
        elif item.gender not in test_score_dict[item.reference_date].keys():
            test_score_dict[item.reference_date][item.gender] = {}
        elif item.domain not in test_score_dict[item.reference_date][item.gender].keys():
            test_score_dict[item.reference_date][item.gender][item.domain] = []
        elif item.characteristics == "Estimated average score":
            test_score_dict[item.reference_date][item.gender][item.domain].append(item.value)
        else:
            pass
    return Response(test_score_dict)




@api_view(['GET'])
def labour_force(request):
    data = {}
    labour_status = LabourForce.objects.all()
    labour_dict = {}
    for item in labour_status:
        if item.reference_date not in labour_dict.keys():
            labour_dict[item.reference_date] = {}
        else:
            labour_dict[item.reference_date][item.labour_force_status] = item.value

    
    labour_key = list(labour_dict["2018/2019"].keys())
    labour_value = list(labour_dict["2018/2019"].values())
    data = {
        'l_keys': labour_key,
        'l_values': labour_value
    }
    return Response(data)


@api_view(['GET'])
def post_enrollment(request):
    data = {}            
    enrollment_data = PostSecondaryEnrollment.objects.all()
    enrollment_dict = {}
    for item in enrollment_data:
        if item.reference_date not in enrollment_dict.keys():
            enrollment_dict[item.reference_date] = {}
        elif item.institution_type == "Total, institution type":
            enrollment_dict[item.reference_date][item.geo] = item.value
        else:
            pass

    enrollment_key = list(enrollment_dict["2019/2020"].keys())
    enrollment_value = list(enrollment_dict["2019/2020"].values())
    data = {
        'e_keys': enrollment_key,
        'e_values': enrollment_value
    }

    return Response(data)


@api_view(['GET'])
def expenditure_college(request):
    data = {}
    expenditure_data = ExpenditureColleges.objects.all()
    expenditure_dict = {}
    for item in expenditure_data:
        if item.reference_date not in expenditure_dict.keys():
            expenditure_dict[item.reference_date] = {}
        elif item.geo not in expenditure_dict[item.reference_date].keys():
            expenditure_dict[item.reference_date][item.geo] = []
        else:
            expenditure_dict[item.reference_date][item.geo].append(item.value)

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
        
    expenditure_value = list(expenditure_dict['2019/2020']['Canada'][1:])

    data = {
        'exp_keys': expenditure_key,
        'exp_values': expenditure_value
    }

    return Response(data)


@api_view(['GET'])
def apprentice_registration(request):
    data = {}
    apprentice_data = ApprenticeshipRegistration.objects.all()
    apprentice_dict = {}
    for item in apprentice_data:
        if item.reference_date not in apprentice_dict.keys():
            apprentice_dict[item.reference_date] = {}
        elif item.trade_groups == "Total major trade groups":
            apprentice_dict[item.reference_date][item.geo] = item.value
        else:
            pass
    
    apprentice_keys = list(apprentice_dict['2020-01-01 00:00:00'].keys())
    apprentice_values = list(apprentice_dict['2020-01-01 00:00:00'].values())
    data = {
        'apr_keys': apprentice_keys,
        'apr_values': apprentice_values
    }

    return Response(data)

@api_view(['GET'])
def unemployment_rate(request):
    data = {}
    unemployment_data = UnemploymentRate.objects.all()
    unemployment_dict = {}
    for item in unemployment_data:
        if item.reference_date not in unemployment_dict.keys():
            unemployment_dict[item.reference_date] = {}
        elif item.characteristics_of_the_population not in unemployment_dict [item.reference_date].keys():
            unemployment_dict[item.reference_date][item.characteristics_of_the_population] = []
           
        else:
            unemployment_dict[item.reference_date][item.characteristics_of_the_population].append(item.percentage)
    
    unemployment_keys = list(unemployment_dict['2018-01-01 00:00:00'].keys())
    unemployment_values = []

    for key, value in unemployment_dict['2018-01-01 00:00:00'].items():
        unemployment_values.append(round(mean(value), 2))
    

    data = {
        'unempl_keys': unemployment_keys,
        'unempl_values': unemployment_values
    }

    return Response(data)



# @csrf_exempt
def data_for_pdf_summary_extractor_page_api_call(request):
    pdf_summaries = []
    results_list = []
    search_keywords = ""
    error_message = ""
    data = {}
    search = 'digital+learning+ontario+public+schools'
    print("The search term that came from react is", request.POST.get('searchterm'))
    if request.method == 'POST' and request.POST.get('searchterm'):
        print("The term is ",request.POST.get('searchterm'))
        search = request.POST.get('searchterm')

        search_list = str(search).split(" ")
        for x in search_list:
            search_keywords+=x+"+"

        search = search_keywords[0:len(search_keywords)-1]
    

    results_list, db_data_found = canadianviews.pdf_finder_retriever(search)

    if len(results_list) == 0:
        error_message = 'Search results not found'
    else: 
        if len(results_list) >= 4:
            print("result values are greater than equal to 5")
            pdf_summaries = canadianviews.read_pdf(results_list[0:4], search, db_data_found)
        
        if len(results_list) == 1 or len(results_list) == 2 or len(results_list) == 3:
            print("result values are less than equal to 3")
            pdf_summaries = canadianviews.read_pdf(results_list, search, db_data_found)

    data = {
        'summaries': pdf_summaries,
        'error': error_message
    }
    return JsonResponse(data)



@api_view(['GET'])
def usa_ethnicity(request):
    
    ethnicity = {}

    states, ethncity_value = kaggleviews.mean_percentage_access_of_black_hispanic(request)
    updated_states = states[:11]
    ethnicity["state"] = updated_states
    ethnicity["value"] = ethncity_value
    ethnicity_json = json.dumps(ethnicity)
    return Response(ethnicity)
    



@api_view(['GET'])
def usa_expenditure(request):

    expenditure = {}
    state, value = kaggleviews.expenditure_per_pupil_in_different_states()
    expenditure["state"] = state
    expenditure["value"] = value
    return Response(expenditure)

@api_view(['GET'])
def usa_county_connection(request):
    county_connection = {}
    county_connection_value, county_district = kaggleviews.percentage_access_in_state("Illinois")
    county_connection["district"] = county_district
    county_connection["value"] = county_connection_value
    return Response(county_connection)


# Test this for user errors

@api_view(['GET'])
def pk_usa_county_connection(request,pk):
    county_connection = {}
    county_connection_value, county_district = kaggleviews.percentage_access_in_state(pk)
    county_connection["district"] = county_district
    county_connection["value"] = county_connection_value
    return Response(county_connection)


@api_view(['GET'])
def usa_statistics(request):
    
    usa_statistics = {}
    numberofdistricts, numberofstates = kaggleviews.totalNumberOfSchoolDistricts()  # statistic 1
    products, numberofproducts = kaggleviews.total_number_of_products()  # statistic 2
    suburb, rural, town, city, type_of_local = kaggleviews.total_locale_type() # statistic 3
    usa_statistics["districts"] = numberofdistricts
    usa_statistics["products"] = numberofproducts
    usa_statistics["locations"] = [suburb, rural, town, city]
    usa_statistics["states"] = numberofstates
    return Response(usa_statistics)




@api_view(['GET'])
def usa_bottom_10_product_engagement(request):
    product_engagement = {}
    bottomProducts, engagementOfLeastProducts, _, _ = kaggleviews.productEngagement()
    product_engagement["bottom_products"] = bottomProducts
    product_engagement["less_engagement"] = engagementOfLeastProducts
    return Response(product_engagement)


@api_view(['GET'])
def usa_top_10_product_engagement(request):
    product_engagement = {}
    _,_, productsOnly, engagementOnly = kaggleviews.productEngagement()
    product_engagement["products"] = productsOnly
    product_engagement["engagement"] = engagementOnly
    return Response(product_engagement)





@api_view(['GET'])
def usa_broadband(request):
    broadband = {}
    broadband_states, broadband_average = kaggleviews.broadband_connection()
    broadband["states"] = broadband_states
    broadband["value"] = broadband_average
    return Response(broadband)



@api_view(['GET'])
def usa_product_engagement_info(request):
    engagement = {}
    engagement_info, time, product_info = kaggleviews.product_engage(60825)
    engagement["engagement_info"] = engagement_info 
    engagement["time"] = time
    engagement["product_info"] = product_info
    return Response(engagement)

# Test this for user errors

@api_view(['GET'])
def pk_usa_product_engagement_info(request,pk):
    engagement = {}
    engagement_info, time, product_info = kaggleviews.product_engage(pk)
    engagement["engagement_info"] = engagement_info 
    engagement["time"] = time
    engagement["product_info"] = product_info
    return Response(engagement)




@api_view(['GET'])
def usa_free_reduced(request):
    
    free_reduced = {}

    states, ethncity_value = kaggleviews.mean_percentage_access_of_black_hispanic(request)
    reduced = kaggleviews.free_reduced()

    reduced_values = list(reduced.values())
    reduced_keys = list(reduced.keys())
    for x, y in reduced.items():
        if math.isnan(y):
            reduced_values.remove(y)
            reduced_keys.remove(x)

    free_reduced["values"] = reduced_values[:10]
    free_reduced["pct_ethnicity"] = ethncity_value[:10]
    free_reduced["states"] = reduced_keys[:10]

    return Response(free_reduced)



def studentPage(request):
    hotspots = []
    page = 'student.html'

    if request.method == 'GET':
        records = Hotspot.objects.all()   
        for item in records:
            hotspots.append({'download': item.download, 'upload': item.upload,  'name': item.name, 'address':item.address})
        
    else:
        search = request.POST.get('searchbox')
        # result = Hotspot.objects.filter(download__contains=search)
        # result = Hotspot.objects.filter(upload__contains=search)
        # result = Hotspot.objects.filter(name__contains=search)
        result = Hotspot.objects.filter(download__gte=search)
        # result = Hotspot.objects.filter(address__contains=search)
        for item in result:
            hotspots.append({'download': item.download, 'upload': item.upload,  'name': item.name, 'address':item.address})
        print(result)
        
       
    context = {'hotspot': hotspots}
    return render(request,page,context)


def getTweets(request):
    tweets = Tweets.objects.all()  
    tweet_list = []
    

    if request.method == 'GET':
        for item in tweets:
            print("The url is", item.url)
            tweet_list.append({'text': item.text, 'category': item.category,  'retweets': item.retweets, 
            'likes':item.likes, "date": item.date, 'url': item.url})

    
    else:
        search = request.POST.get('searchbox')
        search_words = ('Internet', 'Device', 'Mental Health', 'Performance')
        tweets = []
        tweet_list = []
        if (search in search_words):
            tweets = Tweets.objects.filter(category=search)
        for item in tweets:
            tweet_list.append({'text': item.text, 'category': item.category,  'retweets': item.retweets, 'likes':item.likes, "date": item.date, 'url': item.url})
    
    context = { 'tweets': tweet_list}
    template = 'twitter.html'
    # print("The json is",json_tweet)
    return render(request, template, context)
    
    
    
    
    context = { 'tweets': tweet_list}
    template = 'twitter.html'

    return render(request, template, context)


    













