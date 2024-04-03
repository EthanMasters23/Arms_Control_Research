
### New NYT API ###

### - IMPORTS - ###

import json
from pprint import pprint
import requests, re
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go

import os

#checking python version
import sys
# print(sys.version)

### - IMPORTS (END) - ###

import time

start = time.time()

### - query testing - ###

# page  = 0 
# begin_date = 19450101
# end_date = 19451231
# APIkey = "9jleO955LNYEMxbaH5A49adGcBJle43K" # Ethan's API Key
# response_field = 'abstract,web_url,snippet,source,headline,keywords,pub_date,section_name' # list of fields to included in data collection

# requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?&q=arms%20reduction%2C%20arms%20control%2C%20weapons%20disarmament%2C%20nuclear%20disarmament&begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1%20AND%20print_section%3A%22A%22)%20OR%20(subject%3A%22Nuclear%20Weapons%22%20OR%20subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Nuclear%20Tests%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''
# # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1%20AND%20print_section%3A%22A%22)%20AND%20(%22arms%20reduction%22%20OR%20%22arms%20control%22%20OR%20%22weapons%20disarmament%22%20OR%20%22nuclear%20disarmament%22)%20OR%20(subject%3A%22Nuclear%20Weapons%22%20OR%20subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Nuclear%20Tests%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''
# response = requests.get(requestUrl).json()["response"]["meta"]
# pprint(response)

### - query testing (END) - ###

### - Adjust to test number - ###
test1 = 15

################################################## - START DATA COLLECTION - ########################################################

def execute(begin_date,end_date,test2=test1):

    #### TEST RUN ###

    def data_collection():

        ### inputs ###
        APIkey = "NNEVLqcrq6X3waJNf0IixwUaerowCqeR" # Ethan's API Key
        # response_field = 'abstract,web_url,snippet,source,headline,keywords,pub_date,section_name,print_page,print_section,document_type' # list of fields to included in data collection

        ### output ###
        out_data = []

        ### used for test case NNEVLqcrq6X3waJNf0IixwUaerowCqeR15

        weapons_hits = 0
        control_hits = 0 
        reduction_hits = 0

        for page in range(0,101):
            pprint(f"page: {page}")
            if int(re.search(r"^(\d{4})",str(begin_date)).group(1)) <= 1966 or int(re.search(r"^(\d{4})",str(end_date)).group(1)) <= 1966:

                ### Test 3 ###
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?&q=arms%20reduction%2C%20arms%20control%2C%20weapons%20disarmament%2C%20nuclear%20disarmament&begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1%20)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 4 ###
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?&q=arms%20reduction%2C%20arms%20control%2C%20weapons%20disarmament%2C%20nuclear%20disarmament&begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1%20)%20AND%20(%22arms%20reduction%22%20OR%20%22arms%20control%22%20OR%20%22weapons%20disarmament%22%20OR%20%22nuclear%20disarmament%22)%20OR%20(subject%3A%22Nuclear%20Weapons%22%20OR%20subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Nuclear%20Tests%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 5 ###
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?&begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1%20)%20AND%20(%22arms%20reduction%22%20OR%20%22arms%20control%22%20OR%20%22weapons%20disarmament%22%20OR%20%22nuclear%20disarmament%22)%20OR%20(subject%3A%22Nuclear%20Weapons%22%20OR%20subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Nuclear%20Tests%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 6 ###
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?&begin_date={begin_date}&end_date={end_date}&fq=(type_of_material%3A%22Front%20Page%22)%20OR%20(print_page%3A1)%20AND%20(document_type%3A%22article%22)%20AND%20(%22arms%20reduction%22%20OR%20%22arms%20control%22%20OR%20%22weapons%20disarmament%22%20OR%20%22nuclear%20disarmament%22)%20OR%20(subject%3A%22Nuclear%20Weapons%22%20OR%20subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Nuclear%20Tests%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 7 ###  
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?&begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1)%20AND%20(document_type%3A%22article%22)%20AND%20(%22arms%20reduction%22%20OR%20%22arms%20control%22%20OR%20%22weapons%20disarmament%22)%20OR%20(subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 8 ###
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?q=arms%20reduction%2C%20arms%20control%2C%20weapons%20disarmament&begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1)%20AND%20(document_type%3A%22article%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 9 ###
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?q=arms%20reduction%2C%20arms%20control%2C%20weapons%20disarmament&begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1)%20AND%20(document_type%3A%22article%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 10 ### only searching for page 1 not page_section A and adding fq front page capture filter for some reason it wasn't set for > 1977
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?q=arms%20reduction%2C%20arms%20control%2C%20weapons%20disarmament&begin_date={begin_date}&end_date={end_date}&fq=(type_of_material%3A%22Front%20Page%22)%20OR%20(print_page%3A1)%20AND%20(document_type%3A%22article%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 11 ### only searching for page 1 not page_section A and adding fq front page capture filter for some reason it wasn't set for > 1977
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?q=arms%20reduction%2C%20arms%20control%2C%20weapons%20disarmament&begin_date={begin_date}&end_date={end_date}&fq=(type_of_material%3A%22Front%20Page%22)%20OR%20(print_page%3A1)%20AND%20(document_type%3A%22article%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 12 ### same query for < 1980 and > 1980
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1)%20AND%20(news_desk%3A%22Foreign%22%20OR%20news_desk%3A%22Foreign%20Desk%22%20OR%20news_desk%3A%22National%22%20OR%20news_desk%3A%22National%20Desk%22%20OR%20news_desk%3A%22None%22%20OR%20news_desk%3A%22%22)%20AND%20(section_name%3A%22World%22%20OR%20section_name%3A%22Science%22%20OR%20section_name%3A%22U.S.%22%20OR%20section_name%3A%22None%22%20OR%20section_name%3A%22Washington%22%20OR%20section_name%3A%22Archives%22)%20AND%20(%22arms%20reduction%22%20OR%20%22arms%20control%22%20OR%20%22weapons%20disarmament%22%20OR%20%22nuclear%20disarmament%22)%20OR%20(subject%3A%22nuclear%20nonproliferation%20treaty%22%20OR%20subject%3A%22eisenhower%20plan%20('atoms%20for%20peace')%22%20OR%20subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)%20&sort=newest&page={page}&api-key={APIkey}'''
                
                ### Test 13 ### changing to make different for years prior to 1966 (adding armament as subject) NOT READY
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1)%20AND%20(news_desk%3A%22Foreign%22%20OR%20news_desk%3A%22Foreign%20Desk%22%20OR%20news_desk%3A%22National%22%20OR%20news_desk%3A%22National%20Desk%22%20OR%20news_desk%3A%22None%22%20OR%20news_desk%3A%22%22)%20AND%20(section_name%3A%22World%22%20OR%20section_name%3A%22Science%22%20OR%20section_name%3A%22U.S.%22%20OR%20section_name%3A%22None%22%20OR%20section_name%3A%22Washington%22%20OR%20section_name%3A%22Archives%22)%20AND%20(%22arms%20reduction%22%20OR%20%22arms%20control%22%20OR%20%22weapons%20disarmament%22%20OR%20%22nuclear%20disarmament%22)%20OR%20(subject%3A%22armament%22%20OR%20subject%3A%22nuclear%20nonproliferation%20treaty%22%20OR%20subject%3A%22eisenhower%20plan%20('atoms%20for%20peace')%22%20OR%20subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)%20&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 14 ### new approch below ### creating seperate requests to gather data ###
                      
                requestUrl1 = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={begin_date}&end_date={end_date}&fq=(%22weapons%20disarmament%22%)20AND%20(print_page%3A1)%20AND%20(news_desk%3A%22Foreign%22%20OR%20news_desk%3A%22Foreign%20Desk%22%20OR%20news_desk%3A%22National%22%20OR%20news_desk%3A%22National%20Desk%22%20OR%20news_desk%3A%22None%22)&sort=newest&page={page}&api-key={APIkey}'''

                requestUrl2 = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={begin_date}&end_date={end_date}&fq=(%22arms%20control%22%)20AND%20(print_page%3A1)%20AND%20(news_desk%3A%22Foreign%22%20OR%20news_desk%3A%22Foreign%20Desk%22%20OR%20news_desk%3A%22National%22%20OR%20news_desk%3A%22National%20Desk%22%20OR%20news_desk%3A%22None%22)&sort=newest&page={page}&api-key={APIkey}'''

                requestUrl3 = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={begin_date}&end_date={end_date}&fq=(%22arms%20reduction%22%)20AND%20(print_page%3A1)%20AND%20(news_desk%3A%22Foreign%22%20OR%20news_desk%3A%22Foreign%20Desk%22%20OR%20news_desk%3A%22National%22%20OR%20news_desk%3A%22National%20Desk%22%20OR%20news_desk%3A%22None%22)&sort=newest&page={page}&api-key={APIkey}'''

            else:

                ### Test 3 ###                    
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?&q=arms%20reduction%2C%20arms%20control%2C%20weapons%20disarmament%2C%20nuclear%20disarmament&begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1%20AND%20print_section%3A%22A%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 4 ###
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?&q=arms%20reduction%2C%20arms%20control%2C%20weapons%20disarmament%2C%20nuclear%20disarmament&begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1%20AND%20print_section%3A%22A%22)%20AND%20(%22arms%20reduction%22%20OR%20%22arms%20control%22%20OR%20%22weapons%20disarmament%22%20OR%20%22nuclear%20disarmament%22)%20OR%20(subject%3A%22Nuclear%20Weapons%22%20OR%20subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Nuclear%20Tests%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''
                
                ### Test 5 ###
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1%20AND%20print_section%3A%22A%22)%20AND%20(%22arms%20reduction%22%20OR%20%22arms%20control%22%20OR%20%22weapons%20disarmament%22%20OR%20%22nuclear%20disarmament%22)%20OR%20(subject%3A%22Nuclear%20Weapons%22%20OR%20subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Nuclear%20Tests%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 6 ###
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?&begin_date={begin_date}&end_date={end_date}&fq=(type_of_material%3A%22Front%20Page%22)%20OR%20(print_page%3A1%20AND%20print_section%3A%22A%22)%20AND%20(document_type%3A%22article%22)%20AND%20(%22arms%20reduction%22%20OR%20%22arms%20control%22%20OR%20%22weapons%20disarmament%22%20OR%20%22nuclear%20disarmament%22)%20OR%20(subject%3A%22Nuclear%20Weapons%22%20OR%20subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Nuclear%20Tests%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 7 ###
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?&begin_date={begin_date}&end_date={end_date}&fq=(type_of_material%3A%22Front%20Page%22)%20OR%20(print_page%3A1%20AND%20print_section%3A%22A%22)%20AND%20(document_type%3A%22article%22)%20AND%20(%22arms%20reduction%22%20OR%20%22arms%20control%22%20OR%20%22weapons%20disarmament%22)%20OR%20(subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 8 ###
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?q=arms%20reduction%2C%20arms%20control%2C%20weapons%20disarmament&begin_date={begin_date}&end_date={end_date}&fq=(type_of_material%3A%22Front%20Page%22)%20OR%20(print_page%3A1%20AND%20print_section%3A%22A%22)%20AND%20(document_type%3A%22article%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 9 ### no difference from 8, but adding fields (print_page,print_section,document_type)
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?q=arms%20reduction%2C%20arms%20control%2C%20weapons%20disarmament&begin_date={begin_date}&end_date={end_date}&fq=(type_of_material%3A%22Front%20Page%22)%20OR%20(print_page%3A1%20AND%20print_section%3A%22A%22)%20AND%20(document_type%3A%22article%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 10 ### only searching for page 1 not page_section A
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?q=arms%20reduction%2C%20arms%20control%2C%20weapons%20disarmament&begin_date={begin_date}&end_date={end_date}&fq=(type_of_material%3A%22Front%20Page%22)%20OR%20(print_page%3A1)%20AND%20(document_type%3A%22article%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 11 ### only searching for page 1 not page_section A
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?q=arms%20reduction%2C%20arms%20control%2C%20weapons%20disarmament&begin_date={begin_date}&end_date={end_date}&fq=(type_of_material%3A%22Front%20Page%22)%20OR%20(print_page%3A1)%20AND%20(document_type%3A%22article%22)&fl={response_field}&sort=newest&page={page}&api-key={APIkey}'''

                ### Test 12 ### same query for < 1980 and > 1980
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1)%20AND%20(news_desk%3A%22Foreign%22%20OR%20news_desk%3A%22Foreign%20Desk%22%20OR%20news_desk%3A%22National%22%20OR%20news_desk%3A%22National%20Desk%22%20OR%20news_desk%3A%22None%22)%20AND%20(section_name%3A%22World%22%20OR%20section_name%3A%22Science%22%20OR%20section_name%3A%22U.S.%22%20OR%20section_name%3A%22None%22%20OR%20section_name%3A%22Washington%22%20OR%20section_name%3A%22Archives%22)%20AND%20(%22arms%20reduction%22%20OR%20%22arms%20control%22%20OR%20%22weapons%20disarmament%22%20OR%20%22nuclear%20disarmament%22)%20OR%20(subject%3A%22nuclear%20nonproliferation%20treaty%22%20OR%20subject%3A%22eisenhower%20plan%20('atoms%20for%20peace')%22%20OR%20subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)%20&sort=newest&page={page}&api-key={APIkey}'''
                
                ### Test 13 ### 
                # requestUrl = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={begin_date}&end_date={end_date}&fq=(print_page%3A1)%20AND%20(news_desk%3A%22Foreign%22%20OR%20news_desk%3A%22Foreign%20Desk%22%20OR%20news_desk%3A%22National%22%20OR%20news_desk%3A%22National%20Desk%22%20OR%20news_desk%3A%22None%22)%20AND%20(section_name%3A%22World%22%20OR%20section_name%3A%22Science%22%20OR%20section_name%3A%22U.S.%22%20OR%20section_name%3A%22None%22%20OR%20section_name%3A%22Washington%22%20OR%20section_name%3A%22Archives%22)%20AND%20(%22arms%20reduction%22%20OR%20%22arms%20control%22%20OR%20%22weapons%20disarmament%22%20OR%20%22nuclear%20disarmament%22)%20OR%20(subject%3A%22nuclear%20nonproliferation%20treaty%22%20OR%20subject%3A%22eisenhower%20plan%20('atoms%20for%20peace')%22%20OR%20subject%3A%22Arms%20Control%20and%20Limitation%20and%20Disarmament%22%20OR%20subject%3A%22Strategic%20Arms%20Reduction%20Treaty%22)%20&sort=newest&page={page}&api-key={APIkey}'''
                     
                ### Test 14 ### new approch below ### creating seperate requests to gather data ###              

                requestUrl1 = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={begin_date}&end_date={end_date}&fq=(%22weapons%20disarmament%22%)20AND%20(print_page%3A1)%20AND%20(news_desk%3A%22Foreign%22%20OR%20news_desk%3A%22Foreign%20Desk%22%20OR%20news_desk%3A%22National%22%20OR%20news_desk%3A%22National%20Desk%22%20OR%20news_desk%3A%22None%22)&sort=newest&page={page}&api-key={APIkey}'''

                requestUrl2 = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={begin_date}&end_date={end_date}&fq=(%22arms%20control%22%)20AND%20(print_page%3A1)%20AND%20(news_desk%3A%22Foreign%22%20OR%20news_desk%3A%22Foreign%20Desk%22%20OR%20news_desk%3A%22National%22%20OR%20news_desk%3A%22National%20Desk%22%20OR%20news_desk%3A%22None%22)&sort=newest&page={page}&api-key={APIkey}'''

                requestUrl3 = f'''https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={begin_date}&end_date={end_date}&fq=(%22arms%20reduction%22%)20AND%20(print_page%3A1)%20AND%20(news_desk%3A%22Foreign%22%20OR%20news_desk%3A%22Foreign%20Desk%22%20OR%20news_desk%3A%22National%22%20OR%20news_desk%3A%22National%20Desk%22%20OR%20news_desk%3A%22None%22)&sort=newest&page={page}&api-key={APIkey}'''

            ########### test case 14 use only ##############z

            ### first request

            if page == 0:
                response = requests.get(requestUrl1).json()["response"]
                pprint(response["meta"])
                weapons_hits = response['meta']['hits'] / 10
                time.sleep(2)

            if weapons_hits >= page:
                response = requests.get(requestUrl1).json()["response"]
                response = response["docs"]
                time.sleep(2)
                out_data += response     

            ### second request
            
            if page == 0:
                response = requests.get(requestUrl2).json()["response"]
                pprint(response["meta"])
                reduction_hits = response['meta']['hits'] / 10
                time.sleep(2)

            if reduction_hits >= page:
                response = requests.get(requestUrl2).json()["response"]
                response = response["docs"]
                time.sleep(2)
                out_data += response

            ### third request

            if page == 0:
                response = requests.get(requestUrl3).json()["response"]
                pprint(response["meta"])
                control_hits = int(response['meta']['hits']) / 10
                time.sleep(2)

            if control_hits >= page:
                response = requests.get(requestUrl3).json()["response"]
                response = response["docs"]
                time.sleep(2)
                out_data += response

            ############ test case 14 use only #################

            # response = requests.get(requestUrl).json()["response"]

            # if page == 0:
            #     pprint(response["meta"])

            # response = response["docs"]

            # time.sleep(2)

            # out_data += [response]

        return out_data
    
    out_data = data_collection()

    # ## - data storage - ###
    # with open(f'/Volumes/ESD-USB/np_research_app/assets/research_data_output_test_{test2}_{begin_date}-{end_date}.json', 'w') as fp:
    #     json.dump(out_data, fp)

    # ## - data recall - ###
    # with open(f'/Volumes/ESD-USB/np_research_app/assets/research_data_output_test_{test2}_{begin_date}-{end_date}.json', 'r') as fp:
    #     out_data = json.load(fp)

    def cleaning_data(input_data):
        data_dict = {}
        for article in input_data:
            if not article:
                continue
            date = article["pub_date"]
            if re.search(r"(\d{4})-",article["pub_date"]).group(1) in data_dict:
                if article["pub_date"] in data_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)]:
                    if date + article["headline"]["main"] in data_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)]: continue
                    else:
                        data_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)][date + article["headline"]["main"]] = article
                else:
                    data_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)][date] = article

            else:
                data_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)] = {}
                data_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)][date] = article

        return data_dict

    output = cleaning_data(out_data)

    df = pd.DataFrame.from_dict({(i,j): output[i][j]
                           for i in output.keys() 
                           for j in output[i].keys()},
                       orient='index')

    return df

def function_call():

    ### Test case for query capture test 15

    # First Time Period ( 1945 - 1991 > 1000 responses ) #
    begin_date = 19450101 # start date for data collection fromat : {YYYYMMDD}
    end_date = 19521231 # end date for data collection fromat : {YYYYMMDD}
    output_data_first_period = execute(begin_date,end_date)

    # Second Time Period ( 1945 - 1991 > 1000 responses ) #
    begin_date = 19530101 # start date for data collection fromat : {YYYYMMDD}
    end_date = 19591231 # end date for data collection fromat : {YYYYMMDD}
    output_data_second_period = execute(begin_date,end_date)

    # Third Time Period ( 1991 - 2022 > 10000 responses ) #
    begin_date = 19600101 # start date for data collection fromat : {YYYYMMDD}
    end_date = 19651231 # end date for data collection fromat : {YYYYMMDD}
    output_data_third_period = execute(begin_date,end_date)

    # Fourth Time Period ( 1991 - 2022 > 10000 responses ) #
    begin_date = 19660101 # start date for data collection fromat : {YYYYMMDD}
    end_date = 19711231 # end date for data collection fromat : {YYYYMMDD}
    output_data_fourth_period = execute(begin_date,end_date)

    # Fifth Time Period ( 1991 - 2022 > 10000 responses ) #
    begin_date = 19720101 # start date for data collection fromat : {YYYYMMDD}
    end_date = 19771231 # end date for data collection fromat : {YYYYMMDD}
    output_data_fifth_period = execute(begin_date,end_date)

    # Fourth Time Period ( 1991 - 2022 > 10000 responses ) #
    begin_date = 19780101 # start date for data collection fromat : {YYYYMMDD}
    end_date = 19801231 # end date for data collection fromat : {YYYYMMDD}
    output_data_sixth_period = execute(begin_date,end_date)

    # Fourth Time Period ( 1991 - 2022 > 10000 responses ) #
    begin_date = 19800101 # start date for data collection fromat : {YYYYMMDD}
    end_date = 19831231 # end date for data collection fromat : {YYYYMMDD}
    output_data_seventh_period = execute(begin_date,end_date)

    # Fourth Time Period ( 1991 - 2022 > 10000 responses ) #
    begin_date = 19840101 # start date for data collection fromat : {YYYYMMDD}
    end_date = 19861231 # end date for data collection fromat : {YYYYMMDD}
    output_data_eigth_period = execute(begin_date,end_date)

    # Fourth Time Period ( 1991 - 2022 > 10000 responses ) #
    begin_date = 19870101 # start date for data collection fromat : {YYYYMMDD}
    end_date = 19901231 # end date for data collection fromat : {YYYYMMDD}
    output_data_ninth_period = execute(begin_date,end_date)

    # Fourth Time Period ( 1991 - 2022 > 10000 responses ) #
    begin_date = 19910101 # start date for data collection fromat : {YYYYMMDD}
    end_date = 19981231 # end date for data collection fromat : {YYYYMMDD}
    output_data_tenth_period = execute(begin_date,end_date)

    # # Fourth Time Period ( 1991 - 2022 > 10000 responses ) #
    begin_date = 19990101 # start date for data collection fromat : {YYYYMMDD}
    end_date = 20061231 # end date for data collection fromat : {YYYYMMDD}
    output_data_eleventh_period = execute(begin_date,end_date)

    # # Fourth Time Period ( 1991 - 2022 > 10000 responses ) #
    begin_date = 20070101 # start date for data collection fromat : {YYYYMMDD}
    end_date = 20191231 # end date for data collection fromat : {YYYYMMDD}
    output_data_twelvth_period = execute(begin_date,end_date)

    # Fourth Time Period ( 1991 - 2022 > 10000 responses ) #
    begin_date = 20200101 # start date for data collection fromat : {YYYYMMDD}
    end_date = 20230120 # end date for data collection fromat : {YYYYMMDD}
    output_data_thirteenth_period = execute(begin_date,end_date)

    final_output = pd.concat([
        output_data_first_period,output_data_second_period,
        output_data_third_period,output_data_fourth_period,
        output_data_fifth_period, output_data_sixth_period,
        output_data_seventh_period,output_data_eigth_period,
        output_data_ninth_period,output_data_tenth_period,
        output_data_eleventh_period,output_data_twelvth_period,
        output_data_thirteenth_period]).rename_axis(['Year','Publication Date']).sort_index()

    ### end test case for query capture individual test 15

    ### current runtime 866.2649488449097 ###

    # usual code

    # # First Time Period ( 1945 - 1991 > 1000 responses ) #
    # begin_date = 19450101 # start date for data collection fromat : {YYYYMMDD}
    # end_date = 19771231 # end date for data collection fromat : {YYYYMMDD}
    # output_data_first_period = execute(begin_date,end_date)

    # # First Time Period ( 1945 - 1991 > 1000 responses ) #
    # begin_date = 19780101 # start date for data collection fromat : {YYYYMMDD}
    # end_date = 19880101 # end date for data collection fromat : {YYYYMMDD}
    # output_data_second_period = execute(begin_date,end_date)

    # # Second Time Period ( 1991 - 2022 > 10000 responses ) #
    # begin_date = 19880102 # start date for data collection fromat : {YYYYMMDD}
    # end_date = 20221217 # end date for data collection fromat : {YYYYMMDD}
    # output_data_third_period = execute(begin_date,end_date)

    ### usual code 

    # final_output = pd.concat([output_data_first_period,output_data_second_period,output_data_third_period]).rename_axis(['Year','Publication Date']).sort_index()

    pub_date = final_output["pub_date"].str.split("-", expand = True)
    pub_date.drop([2],axis=1,inplace=True)
    pub_date.columns = ["Year","Month"]

    def date_cleaing(value):
        month_dictionary = {'01':'January','02':'Feburary','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}
        return month_dictionary[value]

    pub_date['Month Published'] = pub_date["Month"].apply(date_cleaing)
    final_output["Year Column"], final_output["Month"], final_output["Month Numeric"] = pub_date.values.T

    def subject_cleaning(alist):
        if alist:
            return str([adict['value'] for adict in alist if adict['name'] == 'subject'])

    final_output['subject'] = final_output['keywords'].apply(subject_cleaning)
    
    def headline_main_cleaning(adict):
        if adict:
            return adict['main']

    final_output['main_line'] = final_output['headline'].apply(headline_main_cleaning)

    def headline_print_line_cleaning(adict):
        if adict:
            return adict['print_headline']    

    final_output['print_headline'] = final_output['headline'].apply(headline_print_line_cleaning)
    
    def link_formating(link):
        return f"[Article Link]({link})"
    
    final_output['web_url'] = final_output['web_url'].apply(link_formating)

    final_output.set_index(["Year","Publication Date"],inplace=True) # needed for test case 15 only
    # final_output.to_json(f"/Volumes/ESD-USB/np_research_app/assets/df_research_data_output_test_{test1}_.json", orient='table') etst case 15
    cwd = os.getcwd()
    final_output.to_json(cwd + f"/NP_Research/assets/df_research_data_output_test_{test1}_.json", orient='table')

    return final_output

################################################## - END DATA COLLECTION - ########################################################


################################################## - START DATA VISUALIZATION - ########################################################

def data_visualization():

    cwd = os.getcwd()
    final_output = pd.read_json(cwd + f"/NP_Research/assets/df_research_data_output_test_{test1}_.json", orient='table')

    pprint(final_output)

    article_occurences_df = pd.DataFrame(final_output.groupby(level=['Year']).size())
    article_occurences_df.reset_index(inplace=True)
    article_occurences_df.columns = ["Year","Article Count"]

    template = "plotly_dark"
    px.line(article_occurences_df,x = "Year",y = "Article Count", title=f"Time Series Data Articles/Year Test: {test1}",template=template).show()
    px.bar(article_occurences_df,x="Year", y="Article Count",title=f"Time Series Data Articles/Year Test: {test1}",labels={"variable":"Key"},template=template).show()
    px.scatter(article_occurences_df,x="Year", y="Article Count", marginal_y="box",title=f"Time Series Data Articles/Year Test: {test1}",labels={"variable":"Month"},template=template).show()

################################################## - END DATA VISUALIZATION - ########################################################

### function calls ###
if __name__ == "__main__":
    function_call()
    data_visualization()
    pass

def article_api_module():
    return pd.read_json(f"assets/df_research_data_output_test_{test1}_.json", orient='table')

end = time.time()
print(end - start)