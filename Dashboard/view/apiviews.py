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

from ..models import CountyConnectionInfo
from ..models import LabourForce
from ..models import PostSecondaryEnrollment
from ..models import ExpenditureColleges
from ..models import ParticipationRate
from ..models import UnemploymentRate
from ..models import ApprenticeshipRegistration
from ..models import AverageTestScores
from ..models import SpecialEducation
from ..models import SchoolBoardAchievements
from ..models import PdfSummary
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
from django.http import JsonResponse

def participation_rate_data_for_api_call():
    print("I am being printed")
    data = {}
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
        'p_keys': participation_keys,
        'p_values' : participation_values
    }
    print(data)
    return data




def is_stats_canada_table_updated(productId):
    # The logic to check if a table with a product id is updated, if it is updated then call the associated table methods to make a call to statscan api.
    updated_tables_today_dict = (StatsCan.tables_updated_today())

    for x in updated_tables_today_dict:
        for key in x.keys():
            if key == 'productId' and x[key] == productId:
                return "Updated Today"

    return "Not Updated Today"