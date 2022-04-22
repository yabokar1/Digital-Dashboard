import math
from typing import Protocol

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import json
import requests
import numpy as np
import pandas as pd
import ast
# from .models import LabourForce
from bs4 import BeautifulSoup
from django.http import HttpResponse, HttpResponseRedirect
from ..forms import UserForm, ProfileForm
from ..models import Districts
from ..models import ProductsInfo
from ..models import EngagementInfo
from ..forms import FilterForm
from ..models import StudentFormInfo
from ..models import CountyConnectionInfo

from django.contrib.auth.decorators import login_required
from random import randint

from statistics import mean
from operator import itemgetter


def mean_percentage_access_of_black_hispanic(request):
     
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

def create_district_graph():
    # form = DistrictForm()
    form = FilterForm
    return form

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

def percentage_access_in_state(state):
    state_list = Districts.objects.filter(state=state)
    district_list = []
    county_connection = []
    for x in state_list:
        county_connection.append(x.county_connection)
        district_list.append(x.district_id)

    return county_connection, district_list
    
def avg(li):
    j = 0
    for i in li:
        j = j + i
    return (int(j / len(li)))