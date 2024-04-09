# API Method Driver
import pandas as pd
import logging
import time
import os
import sys
import re

module_path = os.path.join(os.path.dirname(__file__), '..', 'lib')
sys.path.append(module_path)

from api_data_fetcher import ApiDataFetcher
from data_visualization import DataGrapher


class ApiMethodPipeline:
    def __init__(self, API_KEY, START_DATE, END_DATE):
        self.API_KEY = API_KEY
        self.START_DATE = START_DATE
        self.END_DATE = END_DATE
        self.NYT_DATA = pd.DataFrame()
        self.logger = logging.getLogger(type(self).__name__)

    def run(self):
        self.logger.info(f'Starting Regex Method Article Collection ({self.START_DATE}-{self.END_DATE})...')
        fetcher = ApiDataFetcher(
            self.API_KEY,
            self.START_DATE,
            self.END_DATE
        )
        fetcher.fetch_data()
        fetcher.save_data()
        fetcher.build_clean_dict()
        fetcher.convert_to_dataframe()
        fetcher.save_cleaned_data(self.START_DATE, self.END_DATE)
        self.NYT_DATA = fetcher.get_cleaned_data()

        num_years = len(self.NYT_DATA.index.get_level_values('Year').unique())
        num_articles = len(self.NYT_DATA)
        self.logger.info(f"Number of Years: {num_years} Number of Articles: {num_articles}.")
        self.logger.info(f'Finished Regex Method Article Collection ({self.START_DATE}-{self.END_DATE}).')

    def load_data(self):
        fetcher = ApiDataFetcher(
            self.API_KEY,
            self.START_DATE,
            self.END_DATE
        )
        fetcher.reload_cleaned_data(self.START_DATE, self.END_DATE)
        self.NYT_DATA = fetcher.get_cleaned_data()

    def graph_data(self):
        grapher = DataGrapher(self.NYT_DATA)
        grapher.group_by_year()
        grapher.plot_time_series()


if __name__ == '__main__':
    logging.basicConfig(filename='api_method_pipeline_log.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    logger = logging.getLogger(__name__)
    start_time = time.time()

    pipeline = ApiMethodPipeline(
        API_KEY = "9jleO955LNYEMxbaH5A49adGcBJle43K",
        START_DATE = 1945,
        END_DATE = 1946
    )

    # - class methods - #
    pipeline.run()
    pipeline.load_data()
    print(pipeline.NYT_DATA)
    pipeline.graph_data()

    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"Total runtime: {total_time:.2f}" + "\n"*4)