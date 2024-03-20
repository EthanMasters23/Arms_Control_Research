from tqdm import tqdm
import requests
import pandas as pd
import re
import time
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from pprint import pprint
import json

class FetchData:
    def __init__(self, apiKey, startYear, endYear, article_condition, filter_condition):
        self.API_KEY = apiKey
        self.START_YEAR = startYear
        self.END_YEAR = endYear
        self.ARTICLE_CONDITION = article_condition
        self.FILTER_CONDITION = filter_condition

        self.fetched_data = None

    def fetch_article_data(self):
        nytData = {}

        for year in tqdm(range(self.START_YEAR, self.END_YEAR + 1)):
            print(f"Starting article collection for {year}...")
            nytData[year] = {}
            for month in tqdm(range(1, 13)):
                response = requests.get(f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={self.API_KEY}')

                if response.status_code == 200: response = response.json()
                elif response.status_code == 401: raise Exception("Unauthorized request, check api-key is set.")
                elif response.status_code == 429: raise Exception("Too many requests. Reached your per minute or per day rate limit.")
                else: raise Exception("An error occurred:", response.status_code)

                filtered_response = (
                    [article for article in response["response"]["docs"] if self.filter_article(article)]
                    if self.ARTICLE_CONDITION 
                    else [article for article in response["response"]["docs"]]
                )
                nytData[year][month] = (
                    [article for article in filtered_response if self.topic_filter_article(article)]
                    if self.FILTER_CONDITION
                    else filtered_response
                )
                
                time.sleep(2)
            print(f"Finished collecting articles from {year}.")

        self.fetched_data =  nytData
    
    def filter_article(self, article):
        pub_date = article['pub_date']
        pub_date = re.search(r'(\d{4})-\d{2}-\d{2}T',pub_date).group(1)
        article["print_page_found"] = True
        if int(pub_date) <= 1980:
            try:
                if article["print_page"] == "1": return article
            except: 
                article["print_page_found"] = False
                return article
                # print(f"\t\tFailed to find 'print_page' tag from date: {pub_date}. For article information vist {article['web_url']}")
        else:
            try:
                if (article['news_desk'] == 'Foreign Desk' or article['news_desk'] == 'Foreign') or (article['news_desk'] == 'National Desk' or article['news_desk'] == 'National'):
                    if article["print_page"] == "1":
                        return article
            except: print(f"\t\tFailed to find other relevant tags from date: {pub_date}. For article information vist {article['web_url']}")

    def topic_filter_article(self, article):
        pub_date = article['pub_date']
        pub_date = re.search(r'(\d{4})-\d{2}-\d{2}T',pub_date).group(1)

        total_capture = ["arms control and limitation and disarmament",
                        "strategic arms reduction treaty",
                        "nuclear nonproliferation treaty",
                        "eisenhower plan ('atoms for peace')"]

        if int(pub_date) <= 1966:
            nuclear_topics = ["atomic energy",
                              "atomic weapon",
                              "nuclear weapon",
                              "nuclear test"]
            subject_list = ["arms control",
                            "disarmament",
                            "arms unification",
                            "armament"]
            capture_words = ["weapons disarmament",
                            "arms reduction",
                            "arms control",
                            "arms unification",
                            "disarmament",
                            "world arms",
                            "arms inspection"] # ENTER KEYWORDS HERE (maybe 'arms unification')
        else:
            capture_words = ["weapons disarmament",
                            "arms reduction",
                            "arms control",
                            "arms unification"] # ENTER KEYWORDS HERE (maybe 'arms unification')

        if article["keywords"]:
            article_subject = re.sub(r"\s+"," "," ".join([subject["value"] for subject in article["keywords"] if subject['name'] == "subject"]).lower())

            for first_capture in total_capture:
                if first_capture in article_subject:
                    return article

            if int(pub_date) <= 1966:
                for subject in subject_list:
                    if subject in article_subject:
                        for nuclear in nuclear_topics:
                            if nuclear in article_subject:
                                return article

        for word in capture_words:
            if article['abstract']:
                abstract = re.sub(r"\s+"," ",article['abstract'].lower())
                if re.search(fr"{word}",abstract):
                    return article
            if article["snippet"]:
                snippet = re.sub(r"\s+"," ",article["snippet"].lower())
                if re.search(fr"{word}",snippet):
                    return article
            if article["headline"]:
                if article["headline"]["main"]:
                    main = re.sub(r"\s+"," ",article["headline"]["main"].lower())
                    if re.search(fr"{word}",main):
                        return article
                if article["headline"]["print_headline"]:
                    print_headline = re.sub(r"\s+"," ",article["headline"]["print_headline"].lower())
                    if re.search(fr"{word}",print_headline):
                        return article
            if article["lead_paragraph"]:
                lead_paragraph = re.sub(r"\s+"," ",article["lead_paragraph"].lower())
                if re.search(fr"{word}",lead_paragraph):
                    return article
            if article["keywords"]:
                article_subject = re.sub(r"\s+"," "," ".join([subject["value"] for subject in article["keywords"] if subject['name'] == "subject"]).lower())
                if re.search(fr"{word}",article_subject):
                    return article

                        
    def get_data_from_json(self, filePath):
        return pd.read_json(filePath)

    def get_data(self):
        if self.fetched_data == None: raise Exception("Must call on .fetch_article_data() first to generate data.")
        return self.fetched_data