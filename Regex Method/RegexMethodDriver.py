from pprint import pprint
import logging
import time
import pandas as pd

from DataFetcher import FetchData
from ArticleStats import FetchArticleStats
from DataVisualization import DataGrapher


class RegexMethodPipeline():
    def __init__(self):
        self.API_KEY = "9jleO955LNYEMxbaH5A49adGcBJle43K"
        self.START_YEAR = 1945
        self.END_YEAR = 2024
        self.logger = logging.getLogger(type(self).__name__)
        self.NYT_DATA = pd.DataFrame()

    def run_main(self):
        self.logger.info(f'Starting Regex Method Article Collection ({self.START_YEAR}-{self.END_YEAR})...')
        filter_response = input("Filter articles by meta tags? (y/n): ").lower() == 'y'
        criteria_response = input("Filter articles by regex criteria? (y/n): ").lower() == 'y'

        fetcher = FetchData(
            self.API_KEY,
            self.START_YEAR,
            self.END_YEAR,
            filter_response,
            criteria_response
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
                self.END_YEAR)
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
    logging.basicConfig(filename='RegexMethodLog.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    logger = logging.getLogger(__name__)
    start_time = time.time()

    pipeline = RegexMethodPipeline()
    pipeline.run_main()
    pipeline.graph_data()

    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"Total runtime: {total_time:.2f}")