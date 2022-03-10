import math

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import json
import requests
import numpy as np
# from .models import LabourForce
from django.http import HttpResponse, HttpResponseRedirect


def covid_summary():
    url = 'https://api.covid19tracker.ca/summary'
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    json_results = json_data["data"];
    
    context = {}
    for x in json_results:
        context = x

    # context is what we will pass in the render method
    return context

def covid_statistics_by_province_for_each_day(province, year):
    # inputs are province and year
    # https://api.covid19tracker.ca/provinces      This lists the provinces and their code

    url = 'https://api.covid19tracker.ca/reports/province/'+province
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    json_results = json_data["data"]; 
    result_array = []
    for x in json_results:
        if (year in x['date']):
            result_array.append(x)
        
    return result_array


def all_sub_regions(provincecode):
    # input to function is provincecode, output is a list which contains region name and region code
    url = 'https://api.covid19tracker.ca/province/'+provincecode+'/regions'
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    regionsList = []
    # json_results = json_data["data"]

    for x in json_data:
        if x['province'] == provincecode:
            regionsList.append({'name': x['engname'], 'hr_id': x['hr_uid']})
    
    return regionsList

def single_health_region_info(hr_uid):
    url = 'https://api.covid19tracker.ca/reports/regions/'+hr_uid
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    json_results = json_data["data"]; 

    return json_results
