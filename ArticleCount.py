import requests
import pickle
import pandas as pd
import time
import logging


class ArticleCount:
    def __init__(self):
        self.article_data = {}
        self.START_YEAR = 1945
        self.END_YEAR = 2024
        self.API_KEY = "9jleO955LNYEMxbaH5A49adGcBJle43K"
        self.logger = logging.getLogger(type(self).__name__)
    
    def fetch_article_count(self):
        for year in range(self.START_YEAR, self.END_YEAR + 1):
            start = f'{year}0101'
            end = f'{year}1231'
            request_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={start}&end_date={end}&sort=newest&api-key={self.API_KEY}"
            self._processs_request(request_url, year)
            time.sleep(2)

    def _processs_request(self, url, year):
        try:
            response = requests.get(url)
            response.raise_for_status()
            response_data = response.json()["response"]
            self.article_data[year] = response_data['meta']['hits']
        except requests.exceptions.HTTPError as ERROR:
            if response.status_code == 401:
                self.logger.error("Unauthorized request. Make sure api-key is set.")
            elif response.status_code == 429:
                self.logger.error("Too many requests. You reached your per minute or per day rate limit.")
            else:
                self.logger.error(f"HTTP error occurred: {ERROR}")
        except Exception as ERROR:
            self.logger.error(f"Error{time.time}: {ERROR}")
            self.logger.error(f"Could not collect data from {year}")

    def save_article_total(self):
        with open("assets/NYT_Total_Article_Count.json", "wb") as f:
            pickle.dump(self.article_data, f)

    def load_articles_total(self):
        with open("assets/NYT_Total_Article_Count.json", "rb") as f:
            self.article_data = pickle.load(f)

    def to_dataframe(self):
        self.article_data = pd.DataFrame.from_dict(self.article_data, orient='index')

    def to_json(self):
        self.article_data.to_json("assets/NYT_Total_Article_Count_Cleaned.json")

if __name__ == "__main__":
    pipeline = ArticleCount()
    pipeline.fetch_article_count()
    pipeline.save_article_total()
    pipeline.to_dataframe()
    pipeline.to_json()



