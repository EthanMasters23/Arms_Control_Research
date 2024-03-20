from DataFetcher import FetchData
from DataCleaner import CleanData
from ArticleStats import FetchArticleStats


class RegexMethodPipeline:
    def __init__(self):
        self.API_KEY = "9jleO955LNYEMxbaH5A49adGcBJle43K"
        self.START_YEAR = 2022
        self.END_YEAR = 2022

    def run_main(self):
        data_response = input("Use existing saved data? (y/n): ").lower() == 'y'
        filter_response = input("Filter articles by meta tags? (y/n): ").lower() == 'y'
        criteria_response = input("Filter articles by regex criteria? (y/n): ").lower() == 'y'

        nytDataFile = (
            f'assets/NYT_API_DataFrame_REGEX_CLEANED_({self.START_YEAR}-{self.END_YEAR}).json'
            if filter_response and criteria_response
            else f'assets/NYT_API_DataFrame_REGEX_RAW_({self.START_YEAR}-{self.END_YEAR}).json'
        )

        if data_response:
            try:
                fetcher = FetchData(
                    self.API_KEY,
                    self.START_YEAR,
                    self.END_YEAR,
                    filter_response,
                    criteria_response
                )
                nytData = fetcher.get_data_from_json(nytDataFile)
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
            nytData = fetcher.get_data()
            cleaner = CleanData(nytData)
            cleaner.clean_data()
            cleaner.convert_to_dataframe()
            cleaner.save_data(nytDataFile)
            NYT_DATA = cleaner.get_cleaned_data()

        NYT_DATA.describe()

    def run_stats(self):
        article_stats = FetchArticleStats(
            self.API_KEY,
            self.START_YEAR,
            self.END_YEAR,
        )
        article_stats.get_article_stats()
        article_stats.view_article_stats()


if __name__ == "__main__":
    pipeline = RegexMethodPipeline()
    pipeline.run_stats()
