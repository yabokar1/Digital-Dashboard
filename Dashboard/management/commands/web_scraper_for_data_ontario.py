from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import json
import requests
import numpy as np
# from .models import LabourForce
from django.http import HttpResponse, HttpResponseRedirect
from bs4 import BeautifulSoup
import pandas as pd
from ...models import SpecialEducation
from ...models import SchoolBoardAchievements
class Command(BaseCommand):
    help = 'Scrapes data Ontario site'

    def handle(self, *args, **options):        
        self.stdout.write("Hello my web scraper is running in Heroku")
        
        # try:
        url = "https://data.ontario.ca/dataset/expulsion-rates-by-school-board"
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
                                print(val)
                                obj, created = SchoolBoardAchievements.objects.get_or_create(
                                    board=val[0],
                                    city=val[1], grade_ten_osslt_results=val[2], grade_six_eqao_results=val[3], four_year_graduation_rate=val[4])
                                      
        except:
            print("An error occured for scraping the site")
