from tqdm import tqdm
import requests
import re
import time
import json
import logging
import os
import sys

module_path = os.path.join(os.path.dirname(__file__), '..', 'lib')
sys.path.append(module_path)

from data_cleaner import CleanData

class FetchData(CleanData):
    def __init__(self, apiKey, startYear, endYear, article_condition = True, filter_condition = True):
        super().__init__()
        self.API_KEY = apiKey
        self.START_YEAR = startYear
        self.END_YEAR = endYear
        self.ARTICLE_CONDITION = article_condition
        self.FILTER_CONDITION = filter_condition

        self.missing_data = []
        self.logger = logging.getLogger(type(self).__name__)

    def fetch_article_data(self):
        for year in tqdm(range(self.START_YEAR, self.END_YEAR + 1)):
            self.fetched_data[year] = {}
            for month in tqdm(range(1, 13)):
                self._process_response(year, month)

        if self.missing_data:
            self.logger.info(f"Months of missing data: {self.missing_data}.")
            file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"Article_Data_RegexMethod_Missing_Data_({self.START_YEAR}-{self.END_YEAR}).json")
            with open(file_path, 'w') as f:
                json.dump(self.missing_data, f)

    def fetch_missing_data(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"Article_Data_RegexMethod_Missing_Data_({self.START_YEAR}-{self.END_YEAR}).json")
        with open(file_path, 'r') as f:
            self.missing_data = json.load(f)

        for year, month in self.missing_data:
            self._process_response(year, month)

    def _process_response(self, year, month):
        response = False
        url = f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={self.API_KEY}'
        for attempt in range(3):
            try:
                resp = requests.get(url)
                resp.raise_for_status()
                response = resp.json()
                time.sleep(2)
                break
            except (requests.RequestException, ValueError) as e:
                self.logger.error(f"Error fetching data retrying... : {e}")
            time.sleep(2 * attempt + 2)

        if not response:
            self.logger.error(f"Error failed to fetch data from {year}, {month} with url: {url}, Skipping...")
            self.missing_data += [[year,month]]
            return

        filtered_response = (
            [article for article in response["response"]["docs"] if self._filter_article(article)]
            if self.ARTICLE_CONDITION 
            else [article for article in response["response"]["docs"]]
        )

        self.fetched_data[year][month] = (
            [article for article in filtered_response if self._topic_filter_article(article)]
            if self.FILTER_CONDITION
            else filtered_response
        )
    
    def _filter_article(self, article):
        pub_date = article['pub_date']
        pub_date = re.search(r'(\d{4})-\d{2}-\d{2}T',pub_date).group(1)
        article["print_page_found"] = True
        if int(pub_date) <= 1980:
            try:
                if article["print_page"] == "1":
                    return article
            except: 
                article["print_page_found"] = False
                # self.logger.warning(f"Failed to find 'print_page' tag from date: {pub_date}. For article information vist {article['web_url']}")
                try:
                    if (article['news_desk'] == 'Foreign Desk' or article['news_desk'] == 'Foreign') or (article['news_desk'] == 'National Desk' or article['news_desk'] == 'National'):
                        return article
                except:
                    # self.logger.warning(f"Failed to find other relevant tags ('new_desk') from date: {pub_date}. For article information vist {article['web_url']}")
                    return article
        else:
            try:
                if (article['news_desk'] == 'Foreign Desk' or article['news_desk'] == 'Foreign') or (article['news_desk'] == 'National Desk' or article['news_desk'] == 'National'):
                    if article["print_page"] == "1":
                        return article
            except:
                self.logger.warning(f"Failed to find other relevant tags ('new_desk' & 'print_page') from date: {pub_date}. For article information vist {article['web_url']}")
                return article

    @staticmethod
    def _topic_filter_article(article):
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

    def save_data(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"Article_Data_RegexMethod_Raw_({self.START_YEAR}-{self.END_YEAR}).json")
        with open(file_path, 'w') as file:
            json.dump(self.fetched_data, file)

    def reload_data(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"Article_Data_RegexMethod_Raw_({self.START_YEAR}-{self.END_YEAR}).json")
        with open(file_path, 'r') as file:
            self.fetched_data = json.load(file)

    def get_data(self):
        if not self.fetched_data:
            raise Exception("Must call method fetch_article_data() first to generate data.")
        return self.fetched_data