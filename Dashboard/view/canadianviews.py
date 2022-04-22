import math
from typing import Protocol
from MySQLdb import DBAPISet

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import json
import requests
import numpy as np
# from .models import LabourForce
from bs4 import BeautifulSoup
from django.http import HttpResponse, HttpResponseRedirect

# from ..models import CountyConnectionInfo
# from ..models import LabourForce
# from ..models import PostSecondaryEnrollment
# from ..models import ExpenditureColleges
# from ..models import ParticipationRate
# from ..models import UnemploymentRate
# from ..models import ApprenticeshipRegistration
# from ..models import AverageTestScores
# from ..models import SpecialEducation
# from ..models import SchoolBoardAchievements
# from ..models import PdfSummary

from ..models import *
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
import string
import io
from urllib.request import Request, urlopen
from PyPDF2 import PdfFileReader
from gensim.summarization.summarizer import summarize


import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

from pdfminer.high_level import extract_text
# from StringIO import StringIO
from io import StringIO
from io import BytesIO
from urllib.request import urlopen

import urllib.request
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
import re

def labour_force_data():
    try:
        value = is_stats_canada_table_updated(3710010701)
        if (value == "Updated Today"):
            df = stats_can.sc.zip_table_to_dataframe('3710010701')
            df.columns = [c.replace(' ', '_').replace("-", "_") for c in df.columns]
            df = (df[((df.REF_DATE == "2020/2021") | (df.REF_DATE == "2019/2020") |
                    (df.REF_DATE == "2018/2019"))])

            for index, row in df.iterrows():
                val = (row.REF_DATE, row.Age_group, row.Labour_force_status_of_students_and_non_students, row.VALUE)
                if not np.isnan(
                        row.VALUE) and row.Labour_force_status_of_students_and_non_students != "Total labour Force status":
                    obj, created = LabourForce.objects.get_or_create(
                        reference_date=val[0],
                        age_group=val[1], labour_force_status=val[2], value=val[3])
    except:
        pass
                
        
    labour_status = LabourForce.objects.all()
    
    labour_dict = {}
    for item in labour_status:
        if item.reference_date not in labour_dict.keys():
            labour_dict[item.reference_date] = {}
        else:
            labour_dict[item.reference_date][item.labour_force_status] = item.value

    return labour_dict


def post_enrollment_data():
    try:
        value = is_stats_canada_table_updated(3710001801)
        if (value == "Updated Today"):
            df = stats_can.sc.zip_table_to_dataframe('3710001801')
            df.columns = [c.replace(' ', '_').replace("(", "").replace(")", "") for c in df.columns]
        
            df = (df[(df.Gender == 'Total, gender') &
                    (df.Status_of_student_in_Canada == "Total, status of student in Canada") &
                    (df.International_Standard_Classification_of_Education_ISCED ==
                    'Total, International Standard Classification of Education (ISCED)') &
                    (df.Field_of_study == 'Total, field of study') &
                    (df.Registration_status == "Total, registration status") &
                    (df.UOM == 'Number') &
                    ((df.REF_DATE == "2020/2021") | (df.REF_DATE == "2019/2020") | (df.REF_DATE == "2018/2019"))])

            for index, row in df.iterrows():
                val = (row.REF_DATE, row.GEO, row.Institution_type, row.Gender, row.VALUE)
                obj, created = PostSecondaryEnrollment.objects.get_or_create(
                        reference_date=val[0],
                        geo=val[1], institution_type=val[2], gender=val[3],value=val[4])
    except:
        pass
            
    enrollment_data = PostSecondaryEnrollment.objects.all()
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
    try:
        value = is_stats_canada_table_updated(3710002901)
        if (value == "Updated Today"):
            df = stats_can.sc.zip_table_to_dataframe('3710002901')
            df.columns = [c.replace(' ', '_').replace("(", "").replace(")", "") for c in df.columns]
            df = (df[(df.Types_of_funds_and_functions == 'Total funds') &
                    ((df.REF_DATE == "2020/2021") | (df.REF_DATE == "2019/2020") | (df.REF_DATE == "2018/2019"))])
            for index, row in df.iterrows():
                val = (row.REF_DATE, row.GEO, row.Types_of_expenditures,
                    row.VALUE)
                obj, created = ExpenditureColleges.objects.get_or_create(
                        reference_date=val[0],
                        geo=val[1], types_of_expenditure=val[2], value=val[3])
                
    except:
        pass
    expenditure_data = ExpenditureColleges.objects.all()
    expenditure_dict = {}
    for item in expenditure_data:
        if item.reference_date not in expenditure_dict.keys():
            expenditure_dict[item.reference_date] = {}
        elif item.geo not in expenditure_dict[item.reference_date].keys():
            expenditure_dict[item.reference_date][item.geo] = []
        else:
            expenditure_dict[item.reference_date][item.geo].append(item.value)
    return expenditure_dict

# bar graph
def apprentice_registration_data():

    try:
        value = is_stats_canada_table_updated(3710002301)
        if (value == "Updated Today"):
            df = stats_can.sc.zip_table_to_dataframe('3710002301')
            df.columns = [c.replace(' ', '_').replace("(", "").replace(")", "") for c in df.columns]
            df = (df[(df.Age_groups == "Total age groups") & (df.Sex == 'Both sexes') &
                    (df.Registration_status == 'Total registration status') &
                    ((df.REF_DATE == "2020") | (df.REF_DATE == "2019") | (df.REF_DATE == "2018"))])

            for index, row in df.iterrows():
                if not np.isnan(row.VALUE):
                    val = (row.REF_DATE, row.GEO, row.Age_groups, row.Sex, row.Major_trade_groups,
                        row.Registration_status, row.VALUE)
                    obj, created = ApprenticeshipRegistration.objects.get_or_create(
                        reference_date=val[0],
                        geo=val[1], age_groups=val[2], sex=val[3], trade_groups=val[4], registration_status=val[5], value=val[6])
    except:
        pass       
                
    apprentice_data = ApprenticeshipRegistration.objects.all()
    apprentice_dict = {}
    for item in apprentice_data:
        if item.reference_date not in apprentice_dict.keys():
            apprentice_dict[item.reference_date] = {}
        elif item.trade_groups == "Total major trade groups":
            apprentice_dict[item.reference_date][item.geo] = item.value
        else:
            pass
    return apprentice_dict


#  multi bar graph
def avg_test_score_data():
    try:
        value = is_stats_canada_table_updated(3710014901)
        if (value == "Updated Today"):
            df = stats_can.sc.zip_table_to_dataframe('3710014901')
            df.columns = [c.replace(' ', '_').replace("(", "").replace(")", "") for c in df.columns]
            df = (df[(df.REF_DATE == '2018') | (df.REF_DATE == '2015')])
            for index, row in df.iterrows():
                val = (row.REF_DATE, row.Domain,
                    row.Selected_Characteristics, row.Gender,
                    row.VALUE)
                obj, created = AverageTestScores.objects.get_or_create(
                        reference_date=val[0],
                        domain=val[1], characteristics=val[2], gender=val[3], value=val[4])
    except:
        pass            


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

    return test_score_dict


# speedometer
def participation_rate_data():
    try:
        value = is_stats_canada_table_updated(3710010101)
        if (value == "Updated Today"):
            df = stats_can.sc.zip_table_to_dataframe('3710010101')
            df.columns = [c.replace(' ', '_') for c in df.columns]
            df = (df[(df.REF_DATE == '2020/2021')])
            for index, row in df.iterrows():
                if not np.isnan(row.VALUE):
                    val = (row.REF_DATE, row.Age, row.Type_of_institution_attended,
                        row.VALUE)
                    obj, created = ParticipationRate.objects.get_or_create(
                        reference_date=val[0],
                        age=val[1], type_of_institution=val[2], percentage=val[3])
    except:
        pass

    participation_data = ParticipationRate.objects.all()
    participation_dict = {}
    for item in participation_data:
        if item.reference_date not in participation_dict.keys():
            participation_dict[item.reference_date] = {}
        elif item.age not in participation_dict[item.reference_date].keys():
            participation_dict[item.reference_date][item.age] = []
        else:
            participation_dict[item.reference_date][item.age].append(item.percentage)

    return participation_dict

#
def unemployment_rate_data():
    try:
        value = is_stats_canada_table_updated(1410036101)
        if (value != "Updated Today"):
            df = stats_can.sc.zip_table_to_dataframe('1410036101')
            df.columns = [c.replace(' ', '_') for c in df.columns]
            df = (df[((df.REF_DATE == '2018-01-01') | (df.REF_DATE == '2019-01-01') | (df.REF_DATE == '2020-01-01'))])
            for index, row in df.iterrows():
                val = (row.REF_DATE, row.Characteristics_of_the_population_aged_15_and_over,
                    row.Educational_attainment,
                    row.VALUE)
                obj, created = UnemploymentRate.objects.get_or_create(
                        reference_date=val[0],
                        characteristics_of_the_population=val[1], educational_attainment=val[2], percentage=val[3])
    except:
        pass
    unemployment_data = UnemploymentRate.objects.all()
    unemployment_dict = {}
    for item in unemployment_data:
        if item.reference_date not in unemployment_dict.keys():
            unemployment_dict[item.reference_date] = {}
        elif item.characteristics_of_the_population not in unemployment_dict [item.reference_date].keys():
            unemployment_dict[item.reference_date][item.characteristics_of_the_population] = []
           
        else:
            unemployment_dict[item.reference_date][item.characteristics_of_the_population].append(item.percentage)
    
    
    return unemployment_dict


def is_stats_canada_table_updated(productId):
    # The logic to check if a table with a product id is updated, if it is updated then call the associated table methods to make a call to statscan api.
    updated_tables_today_dict = (StatsCan.tables_updated_today())

    for x in updated_tables_today_dict:
        for key in x.keys():
            if key == 'productId' and x[key] == productId:
                return "Updated Today"

    return "Not Updated Today"

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
    # print(df.columns)
    df = df[['REF_DATE', 'Online_activities', 'Gender', 'Age_group', 'VALUE']]
    # print(df)

    # print(is_stats_canada_table_updated(2210013701))


r = requests.get("https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=covid+impact+on+digital+learning+ontario&oq=")

soup = BeautifulSoup(r.text, 'html.parser')

list_pdf_href = []


# def pdf_finder():
#     string_PDF = "[PDF]"
#     results = soup.find_all('div', attrs={'class': 'gs_or_ggsm'})
#     print("i am about to print")
#     for r in results:
#         children = r.findChildren('a', recursive=False)
#         for child in children:
#             if (string_PDF in str(child)):
#                 list_pdf_href.append(child['href'])
#                 print(child['href'])

#     return list_pdf_href


def read_pdf(pdfs_list, searchterm, db_data_found):
    result = []
    if db_data_found == True:
        print("Yes data is found from db and ready to be shown on front end")
        result = pdfs_list
        print("Result right before sending to front end from db part is", result)
    else:
        print("No reading data manually from the api call")
        # list = [{'pdf_title': 'A survey of language learning/teaching with an overview of activities in Italy during the COVID-19 pandemic', 'authors': 'L Cinganotto,T Lamb', 'url': 'https://www.researchgate.net/profile/Letizia-Cinganotto/publication/358877791_A_SURVEY_OF_LANGUAGE_LEARNINGTEACHING_WITH_AN_OVERVIEW_OF_ACTIVITIES_IN_ITALY_DURING_THE_COVID-19_PANDEMIC/links/621a0187579f1c04171b277d/A-SURVEY-OF-LANGUAGE-LEARNING-TEACHING-WITH-AN-OVERVIEW-OF-ACTIVITIES-IN-ITALY-DURING-THE-COVID-19-PANDEMIC.pdf'}, {'pdf_title': 'Digital Gaps Influencing the Online Learning of Rural Students in Secondary Education: A Systematic Review', 'authors': 'VA Samane-Cutipa, AM Quispe-Quispe…\xa0- world - ijiet.org', 'url': 'http://www.ijiet.org/online/IJIET-4050.pdf'}, {'pdf_title': 'An overview of effects of COVID-19 on mobility and lifestyle: 18 months since the outbreak', 'authors': 'A de Palma,S Vosough', 'url': 'https://thema.u-cergy.fr/IMG/pdf/2022-04.pdf'}]
        
        # The result which we are getting as result of scraping
        print("Result from API call are", pdfs_list)
        
        # https://stackoverflow.com/questions/62157733/open-a-pdf-from-a-url-with-pdfminer-six

        # Read the text from each pdf. Loop represents going through each pdf
        for i in range(len(pdfs_list)):
            resource_manager = PDFResourceManager()
            fake_file_handle = StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)    
            user_agent = ''
            if user_agent == None:
                user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
            headers = {'User-Agent': user_agent}
            try:
                request = urllib.request.Request(pdfs_list[i]['url'], data=None, headers=headers)

                response = urllib.request.urlopen(request).read()
            

                fb = BytesIO(response)

                page_interpreter = PDFPageInterpreter(resource_manager, converter)

                for page in PDFPage.get_pages(fb,
                                            caching=True,
                                            check_extractable=True):
                    page_interpreter.process_page(page)


                text = fake_file_handle.getvalue()

                # close open handles
                fb.close()
                converter.close()   
                fake_file_handle.close()

                if text:
                    text = text.replace(u'\xa0', u' ')

                # Preprocessing
                content = str(text).replace("\n", "")
                cleaned_text = " ".join(content.split())

                values = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")
                for item in cleaned_text:
                    if item not in values:
                        my_string = cleaned_text.replace(item, "")
                
                print("----------------------------------------------------------------------------------")
                
                # Calling the summary method
                summary_of_webpage = text_summarize(my_string,0.01)
                pdfs_list[i]['summary'] = summary_of_webpage

            except:
                print("An error happened")
        for i in range(len(pdfs_list)):
            if "summary" in pdfs_list[i]:
                result.append(pdfs_list[i])
            
        # To insert data to db
        if (result):
            PdfSummary.objects.create(search_keyword=searchterm, data=result)
            
            # send data to template to show on front end

    return result




    # for i in range(len(pdfs_list)):
    #     remote_file = urlopen(Request(pdfs_list[i]['url'], headers={'User-Agent': 'Mozilla/5.0'})).read()
    #     memory_file = io.BytesIO(remote_file)
    #     pdf_file = PdfFileReader(memory_file)
    #     raw_content = ""
    #     num_of_pages = pdf_file.numPages
    #     print("The num of pages is", num_of_pages)

    #     for j in range(num_of_pages):
    #         print(j)
    #         single_page = pdf_file.getPage(j)
    #         page_content = single_page.extractText()
    #         raw_content+= page_content
    #         print(j, "----------------------------------------------------")

    #     content = str(raw_content).replace("\n", "")
    #     cleaned_text = " ".join(content.split())
    #     print("The summary is presented below",text_summarize(cleaned_text,0.01))
    #     print("The number of pages in pdf is", num_of_pages)
    #     print("the number of words in summary is", len(text_summarize(cleaned_text,0.05).split()))

      
        

# https://www.activestate.com/blog/how-to-do-text-summarization-with-python/
def text_summarize(text, per):
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 1500000
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary




def pdf_finder_retriever(search_term):
    # previouslyusedurl = https://scholar.google.com/scholar?q=covid+impact+on+digital+learning+ontario&hl=en&as_sdt=0,5&as_ylo=2022&as_rr=1
    search_keywords = search_term
    # Search will be in format ***+***+****
    list_of_search_words = str(search_keywords).split("+")
    records = PdfSummary.objects.all()
    results_array = []
    db_data_found = False

    for record in records:
        if str(search_keywords).lower() == str(record.search_keyword).lower():
            results_array = record.data
            print("records were found")
            db_data_found = True

    if not results_array:
        db_data_found = False
        URL = "http://api.proxiesapi.com"
    
        # insert your auth key here
        auth_key = "0a2bf50a80bfbd833e08c3221ce52512_sr98766_ooPq87"
        url = "https://scholar.google.com/scholar?hl=en&num=15&as_sdt=0%2C5&q="+search_keywords+"+filetype%3Apdf&btnG="
        
        # defining a params dict for the parameters to be sent to the API 
        PARAMS = {'auth_key':auth_key, 'url':url} 
        
        # sending get request and saving the response as response object 
        r = requests.get(url = URL, params = PARAMS) 
        # r = requests.get("https://scholar.google.com/scholar?q=covid+impact+on+digital+learning+ontario&hl=en&as_sdt=0,5&as_ylo=2022&as_rr=1")
        
        
        # Using beautifulsoup to get all the urls, author name and title in a list. Returns an array of object i.e JSON.
        soup = BeautifulSoup(r.text, 'html.parser')
        url_list = []
        # results_array = []
        authors = ""
        results = soup.find_all('h3', attrs={'class': 'gs_rt'})
        print("The results are", results)
        i = 0
        for r in results:
            i = i + 1
            spanchildren = r.findChildren('span', recursive=False)
            for child in spanchildren:
                spangs = child.find("span", { "class" : "gs_ct1" })
                if "[PDF]" in str(spangs.string):
                    valid_url = spangs.findNext('a')
                    title = spangs.findNext('a').text
                    print("The title of found pdf is",spangs.findNext('a').text)
                    print("The url of found pdf is", valid_url['href'])
                    href_link = valid_url['href']
                    url_list.append(valid_url['href'])
                    authors_div = r.findNext("div")
                    authors_array = authors_div.findChildren('a', recursive=False)
                    if not authors_array:
                        if (authors_div.text):
                            authors = authors_div.text
                            results_array.append({'pdf_title': title, 'authors': authors, 'url': href_link})
                            print("The authors are", authors)
                    else:
                        authors = ""
                        for author in authors_array:
                            authors = authors + author.text + ","
                        print("The authors are", authors[0:len(authors)-1])
                        results_array.append({'pdf_title': title, 'authors': authors[0:len(authors)-1], 'url': href_link})
                  
    return results_array, db_data_found    



def getHotspots(request):
    hotspots = []
    records = Hotspot.objects.all()   
    for item in records:
        hotspots.append({'download': item.download, 'upload': item.upload,  'name': item.name, 'address':item.address})





    

def getTweets(request):
    tweets = Tweets.objects.all()  
    tweet_list = []
    

    if request.method == 'GET':
        for item in tweets:
            tweet_list.append({'text': item.text, 'category': item.category,  'retweets': item.retweets, 
            'likes':item.likes, "date": item.date})

    
    if request.method == 'POST':
        search = request.POST.get('searchbox')
        search_words = ('Internet', 'Device', 'Mental Health', 'Performance')
        tweets = []
        tweet_list = []
        if (search in search_words):
            tweets = Tweets.objects.filter(category=search)
        for item in tweets:
            tweet_list.append({'text': item.text, 'category': item.category,  'retweets': item.retweets, 'likes':item.likes, "date": item.date})
    
    context = { 'tweets': tweet_list}
    template = 'twitter.html'
    # print("The json is",json_tweet)
    return render(request, template, context)
    
    
    
    
    context = { 'tweets': tweet_list}
    template = 'twitter.html'

    return render(request, template, context)


