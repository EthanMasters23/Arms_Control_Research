# Api Data Fetcher
import time
import os
import sys
import logging
import re
import requests
import datetime
import json
from tqdm import tqdm

module_path = os.path.join(os.path.dirname(__file__), '..', 'lib')
sys.path.append(module_path)

from data_cleaner import CleanData

class ApiDataFetcher(CleanData):
    def __init__(self, api_key, start_date, end_date):
        super().__init__()
        self.API_KEY = api_key
        self.START_DATE = start_date
        self.END_DATE = end_date
        self.logger = logging.getLogger(type(self).__name__)
        self.fetched_data = []
        self.missing_data = []

    def fetch_data(self):
        response_field = "headline,pub_date,web_url,keywords"
        search_terms = ["arms control", "weapons disarmament", "arms reduction", "nuclear disarmament", "nuclear arms control", "nuclear proliferation", "nuclear non-proliferation treaty", "nuclear deterrence", "nuclear proliferation treaty"]
        contextual_terms = ["nuclear weapons", "atomic weapons", "nuclear warheads", "strategic arms reduction", "treaty on the non-proliferation of nuclear weapons", "disarmament agreements", "nuclear testing", "nuclear policy", "nuclear security", "nuclear strategy", "nuclear proliferation risks", "nuclear deterrence policy", "nuclear security measures", "nuclear threat assessment"]

        self.logger.info(f"Search terms: {search_terms}.")
        self.logger.info(f"Contexual terms: {contextual_terms}.")
        for year in tqdm(range(self.START_DATE, self.END_DATE + 1)):
            begin_date = f"{year}0101"
            end_date = f"{year}1231"

            for search_term in search_terms:
                url = self._construct_url(search_term, begin_date, end_date, response_field)
                self._fetch_articles(url)

            for context_term in contextual_terms:
                url = self._construct_url(context_term, begin_date, end_date, response_field)
                self._fetch_articles(url)

    def _construct_url(self, term, begin_date, end_date, response_field):
        base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
        query_params = {
            'q': term,
            'begin_date': begin_date,
            'end_date': end_date,
            'fq': '(type_of_material%3A%22Front%20Page%22)%20OR%20(print_page%3A1)%20AND%20(document_type%3A%22article%22)',
            'fl': response_field,
            'sort': 'newest',
            'page': 1,
            'api-key': self.API_KEY
        }
        return f"{base_url}?{'&'.join([f'{k}={v}' for k, v in query_params.items()])}"

    def _fetch_articles(self, url):
        response = self._process_response(url)
        if not response:
            return

        hits = response['response']['meta']['hits']
        if hits > 1000:
            self._handle_large_response(url, hits)
        elif hits > 10:
            self.fetched_data += [article for article in response["response"]["docs"] if article not in self.fetched_data]
            self._paginate_pages(url, hits)
        elif hits > 0:
            self.fetched_data += [article for article in response["response"]["docs"] if article not in self.fetched_data]

    def _process_response(self, url):
        pattern_begin = r'&begin_date=(\d{8})&'
        pattern_end = r'&end_date=(\d{8})&'
        begin_date = re.search(pattern_begin, url).group(1)
        end_date = re.search(pattern_end, url).group(1)
        for attempt in range(3):
            try:
                resp = requests.get(url)
                resp.raise_for_status()
                response = resp.json()
                time.sleep(2 * attempt + 2)
                return response
            except (requests.RequestException, ValueError) as e:
                self.logger.error(f"Error fetching data retrying... : {e}")
            time.sleep(2 * attempt + 2)
        self.logger.error(f"Error failed to fetch data from {begin_date} - {end_date} with url: {url}")
        self.missing_data += [[begin_date, end_date]]
        return None

    def _handle_large_response(self, url, hits):
        pattern_begin = r'&begin_date=(\d{8})&'
        pattern_end = r'&end_date=(\d{8})&'
        begin_date = re.search(pattern_begin, url).group(1)
        end_date = re.search(pattern_end, url).group(1)
        begin_date_dt = datetime.datetime.strptime(begin_date, "%Y%m%d")
        end_date_dt = datetime.datetime.strptime(end_date, "%Y%m%d")
        time_factor = 2

        while begin_date_dt.month != end_date_dt.month:
            new_end_date_dt = begin_date_dt + (end_date_dt - begin_date_dt) / (time_factor)
            new_end_date = new_end_date_dt.strftime("%Y%m%d")
            url = re.sub(r'begin_date=\d{8}', f'begin_date={begin_date}', url)
            url = re.sub(r'end_date=\d{8}', f'end_date={new_end_date}', url)
            response = self._process_response(url)

            if not response:
                self.logger.error(f"\tFailed to fetch large data response for (({begin_date_dt.strftime('%Y%m%d')} - {new_end_date}) - {end_date}). Skipping...")
                return

            hits = response['response']['meta']['hits']
            if hits <= 1000:
                time_factor = 2
                self._fetch_articles(url)
                begin_date_dt = end_date_dt
                end_date_dt = datetime.datetime.strptime(end_date, "%Y%m%d")
            else:
                time_factor += 1

            if time_factor >= 6:
                self.logger.warning("Maximum iterations reached without satisfying loop condition.")
                break

    def _paginate_pages(self, url, total_hits):
        pattern = r"&page=\d+&"
        for page in range(2, int(total_hits // 10) + 2):
            url = re.sub(pattern, f"&page={page}&", url)
            response = self._process_response(url)
            if not response:
                continue
            self.fetched_data += [article for article in response["response"]["docs"] if article not in self.fetched_data]

    def save_data(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"Article_Data_ApiMethod_Raw_({self.START_DATE}-{self.END_DATE}).json")
        with open(file_path, 'w') as file:
            json.dump(self.fetched_data, file)

    def reload_data(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"Article_Data_ApiMethod_Raw_({self.START_DATE}-{self.END_DATE}).json")
        with open(file_path, 'r') as file:
            self.fetched_data = json.load(file)

    def get_data(self):
        if not self.fetched_data:
            raise Exception("Must call method fetch_data() first to generate data.")
        return self.fetched_data