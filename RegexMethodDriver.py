from DataFetcher import FetchData
from ArticleStats import FetchArticleStats
from pprint import pprint
import logging
import time

class RegexMethodPipeline():
    def __init__(self):
        self.API_KEY = "9jleO955LNYEMxbaH5A49adGcBJle43K"
        self.START_YEAR = 1945
        self.END_YEAR = 2024
        self.logger = logging.getLogger(__name__ + '.' + self.__class__.__name__)

    def load_main(self):
        try:
            fetcher = FetchData(
                self.API_KEY,
                self.START_YEAR,
                self.END_YEAR
            )
            fetcher.reload_cleaned_data(self.START_YEAR, self.END_YEAR)
            NYT_DATA = fetcher.get_cleaned_data()
        except FileNotFoundError:
            raise FileNotFoundError
        
        pprint(NYT_DATA)

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
        NYT_DATA = fetcher.get_cleaned_data()

        num_years = len(NYT_DATA.index.get_level_values('Year').unique())
        num_articles = len(NYT_DATA)
        self.logger.info(f"Number of Years: {num_years} Number of Articles: {num_articles}.")
        self.logger.info(f'Finished Regex Method Article Collection ({self.START_YEAR}-{self.END_YEAR}).')

        pprint(NYT_DATA)

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
    
    def load_stats(self):
        fetcher = FetchArticleStats(
                self.API_KEY,
                self.START_YEAR,
                self.END_YEAR)
        fetcher.reload_article_stats()
        fetcher.view_article_stats()



if __name__ == "__main__":
    logging.basicConfig(filename='RegexMethodLog.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    start_time = time.time()
    pipeline = RegexMethodPipeline()
    pipeline.run_main()
    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"Total runtime: {total_time:.2f}")



with open('RegexMethodLog.log', 'r') as file:
    log_contents = file.read()
    print(log_contents)























# ------ OLD VERSION --------- #
    
class RegexMethodPipelineV2():
    def __init__(self):
        self.API_KEY = "9jleO955LNYEMxbaH5A49adGcBJle43K"
        self.START_YEAR = 1945
        self.END_YEAR = 2023

    def run_main(self):
        data_response = input("Use existing saved data? (y/n): ").lower() == 'y'
        filter_response = input("Filter articles by meta tags? (y/n): ").lower() == 'y'
        criteria_response = input("Filter articles by regex criteria? (y/n): ").lower() == 'y'

        if data_response:
            try:
                fetcher = FetchData(
                    self.API_KEY,
                    self.START_YEAR,
                    self.END_YEAR,
                    filter_response,
                    criteria_response
                )
                NYT_DATA = fetcher.reload_data()
            except FileNotFoundError:
                raise FileNotFoundError
        else:
            fetcher = FetchData(
                self.API_KEY,
                self.START_YEAR,
                self.END_YEAR,
                filter_response,
                criteria_response
            )
            fetcher.fetch_article_data()
            cleaner = CleanData(fetcher)
            cleaner.format_data_dict()
            cleaner.convert_to_dataframe()
            cleaner.save_cleaned_data()
            NYT_DATA = cleaner.get_cleaned_data()

        NYT_DATA.describe()

    def run_stats(self):
        load_stats_input = input("Load existing data? (y/n): ").lower() == "y"

        if load_stats_input:
            fetcher = FetchArticleStats(
                self.API_KEY,
                self.START_YEAR,
                self.END_YEAR
            )
            fetcher.reload_article_stats()
            fetcher.view_article_stats()
        else:
            fetcher = FetchArticleStats(
                self.API_KEY,
                self.START_YEAR,
                self.END_YEAR 
            )
            fetcher.get_article_stats()
            fetcher.save_article_stats()
            fetcher.view_article_stats()