from pprint import pprint
import logging
import time
import pandas as pd
import os
import sys
import re

module_path = os.path.join(os.path.dirname(__file__), '..', 'lib')
sys.path.append(module_path)

from regex_data_fetcher import FetchData
from article_stats_fetcher import FetchArticleStats
from data_visualization import DataGrapher


class RegexMethodPipeline():
    def __init__(self, API_KEY, START_YEAR, END_YEAR):
        self.API_KEY = API_KEY
        self.START_YEAR = START_YEAR
        self.END_YEAR = END_YEAR
        self.logger = logging.getLogger(type(self).__name__)
        self.NYT_DATA = pd.DataFrame()

    def run_main(self):
        self.logger.info(f'Starting Regex Method Article Collection ({self.START_YEAR}-{self.END_YEAR})...')

        fetcher = FetchData(
            self.API_KEY,
            self.START_YEAR,
            self.END_YEAR,
            input("Filter articles by meta tags? (y/n): ").lower() == 'y',
            input("Filter articles by regex criteria? (y/n): ").lower() == 'y'
        )
        fetcher.fetch_article_data()
        fetcher.save_data()
        fetcher.format_data_dict()
        fetcher.convert_to_dataframe()
        fetcher.save_cleaned_data(self.START_YEAR, self.END_YEAR)
        self.NYT_DATA = fetcher.get_cleaned_data()

        num_years = len(self.NYT_DATA.index.get_level_values('Year').unique())
        num_articles = len(self.NYT_DATA)
        self.logger.info(f"Number of Years: {num_years} Number of Articles: {num_articles}.")
        self.logger.info(f'Finished Regex Method Article Collection ({self.START_YEAR}-{self.END_YEAR}).')

        pprint(self.NYT_DATA)

    def run_stats(self):
        fetcher = FetchArticleStats(
                self.API_KEY,
                self.START_YEAR,
                self.END_YEAR
                )
        self.logger.info('Running Article Statistics...')
        fetcher.get_article_stats()
        fetcher.save_article_stats()
        fetcher.view_article_stats()
        self.logger.info('Fnished Article Statistics.')

    def load_main(self):
        try:
            fetcher = FetchData(
                self.API_KEY,
                self.START_YEAR,
                self.END_YEAR
            )
            fetcher.reload_cleaned_data(self.START_YEAR, self.END_YEAR)
            self.NYT_DATA = fetcher.get_cleaned_data()
        except FileNotFoundError:
            raise FileNotFoundError
        
        pprint(self.NYT_DATA)
    
    def load_stats(self):
        fetcher = FetchArticleStats(
                self.API_KEY,
                self.START_YEAR,
                self.END_YEAR)
        fetcher.reload_article_stats()
        fetcher.view_article_stats()

    def graph_data(self):
        grapher = DataGrapher(self.NYT_DATA)
        grapher.group_by_year()
        grapher.plot_time_series()
        


if __name__ == "__main__":
    logging.basicConfig(filename='regex_method_pipeline_log.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    logger = logging.getLogger(__name__)
    start_time = time.time()

    pipeline = RegexMethodPipeline(
        API_KEY = "9jleO955LNYEMxbaH5A49adGcBJle43K",
        START_YEAR = 1945,
        END_YEAR = 1946
    )
    pipeline.run_main()
    pipeline.load_main()
    pipeline.graph_data()
    pipeline.run_stats()
    pipeline.load_stats()

    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"Total runtime: {total_time:.2f}")