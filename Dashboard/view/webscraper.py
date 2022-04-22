import math

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import json
import requests
import numpy as np
# from .models import LabourForce
from django.http import HttpResponse, HttpResponseRedirect
from bs4 import BeautifulSoup
import pandas as pd
from ..models import SpecialEducation
from ..models import SchoolBoardAchievements

def webscraperfordataontario():
    # works for this    https://data.ontario.ca/dataset/school-information-and-student-demographics
    # https://data.ontario.ca/dataset/online-learning-course-enrolment-totals-by-course
    url = "https://data.ontario.ca/dataset/special-education-enrolment-by-exceptionality"

    urls = ['https://data.ontario.ca/dataset/special-education-enrolment-by-exceptionality', 'https://data.ontario.ca/dataset/school-board-achievements-and-progress']
    try:

        for i in range(len(urls)):
            if (i == 0):
                result = requests.get(urls[i])

                doc = BeautifulSoup(result.text, "html.parser")

                resource = doc.find_all('a', class_="resource-url-analytics btn btn-primary dataset-download-link")
                download_href = resource[0]['href']

                if str(download_href).endswith('txt') or str(download_href).endswith('csv'):
                    df = pd.read_csv(download_href, sep="|")
                
                elif str(download_href).endswith('xlsx'):
                    df = pd.read_excel(download_href)
                
                if not df.empty:
                    df = df.dropna()
                    df.columns = [c.replace(' ', '_') for c in df.columns]
                    for index, row in df.iterrows():
                        if (row.Area_of_Exceptionality != "Total"):
                            val = (row.Academic_Year, row.Area_of_Exceptionality,
                            row.Elementary_Special_Education_Enrolment,
                            row._Secondary_Special_Education_Enrolment,
                            row.Total_Special_Education_Enrolment)
                            print(val)
                            obj, created = SpecialEducation.objects.get_or_create(
                            academic_year=val[0],
                            exceptionality=val[1], elementary_enrollment=val[2], secondary_enrollment=val[3], total_enrollment=val[4])

            if (i == 1):
               result = requests.get(urls[i])
               doc = BeautifulSoup(result.text, "html.parser")

               resource = doc.find_all('a', class_="resource-url-analytics btn btn-primary dataset-download-link")
               download_href = resource[0]['href']

               if str(download_href).endswith('txt') or str(download_href).endswith('csv'):
                 df = pd.read_csv(download_href, sep="|")
            
               elif str(download_href).endswith('xlsx'):
                 df = pd.read_excel(download_href)
            
               if not df.empty:
                    df = df.dropna()
                    df.columns = [c.replace(' ', '_') for c in df.columns]
                    df = df[['Board_Name', 'City', 'Grade_10_OSSLT_Results', 'Grade_6_EQAO_Reading_Results', 'Four_Year_Graduation_Rate']]
                    print(df.columns)
                    for index, row in df.iterrows():
                        val = (row.Board_Name, row.City,
                        row.Grade_10_OSSLT_Results,
                        row.Grade_6_EQAO_Reading_Results,
                        row.Four_Year_Graduation_Rate)
                        obj, created = SchoolBoardAchievements.objects.get_or_create(
                            board=val[0],
                            city=val[1], grade_ten_osslt_results=val[2], grade_six_eqao_results=val[3], four_year_graduation_rate=val[4])
                         
            
    except:
        print("An error occured for scraping the site")


def lastUpdatedDateforResource(url):

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    resource = doc.find_all('p', class_="description details")
    ptag = resource[0]
    ptag.find('span').decompose()
    last_updated_date =  (str(ptag.text).replace("|", "").replace("Last Updated:", "").strip())
    
    return last_updated_date

def special_education_data():
    special_education_data = SpecialEducation.objects.all()
    exceptionality_list = []
    elementary_list = []
    secondary_list = []
    total_list = []

    
    for items in special_education_data:
        if items.academic_year == '2020-2021':
            if items.exceptionality:
                exceptionality_list.append(items.exceptionality)
            if items.elementary_enrollment:
                elementary_list.append(items.elementary_enrollment)
            if items.secondary_enrollment:
                secondary_list.append(items.secondary_enrollment)
            if items.total_enrollment:
                total_list.append(items.total_enrollment)

    return exceptionality_list, elementary_list, secondary_list, total_list


def school_board_achievements_data():
    board_achievements_data = SchoolBoardAchievements.objects.all()
    board_list = []
    grade_ten_osslt_list = []
    grade_six_eqao_list = []
    four_year_grad_list = []

    for items in board_achievements_data:
        if items.board:
            board_list.append(items.board)
        if items.grade_ten_osslt_results:
            grade_ten_osslt_list.append(items.grade_ten_osslt_results)
        if items.grade_six_eqao_results:
            grade_six_eqao_list.append(items.grade_six_eqao_results)     
        if items.four_year_graduation_rate:
            four_year_grad_list.append(items.four_year_graduation_rate)
    
    return board_list, grade_ten_osslt_list, grade_six_eqao_list, four_year_grad_list


    