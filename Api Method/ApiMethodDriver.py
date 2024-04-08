# API Method Driver
import pandas as pd
import logging
import time

from ApiDataFetcher import ApiDataFetcher
from DataVisualization import DataGrapher


class ApiMethodPipeline:
    def __init__(self):
        self.API_KEY = "9jleO955LNYEMxbaH5A49adGcBJle43K"
        self.START_DATE = 1945
        self.END_DATE = 2024
        self.NYT_DATA = pd.DataFrame()
        self.logger = logging.getLogger(type(self).__name__)

    def pull_data(self):
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

    def reload_data(self):
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
    logging.basicConfig(filename='ApiMethodLog.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    logger = logging.getLogger(__name__)
    start_time = time.time()

    pipeline = ApiMethodPipeline()
    pipeline.pull_data()
    # pipeline.reload_data()
    pipeline.graph_data()

    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"Total runtime: {total_time:.2f}" + "\n"*4)