import pandas as pd
import re
import logging
import os

class CleanData():
    def __init__(self):
        self.fetched_data = {}
        self.cleaned_data = {}
        self.logger = logging.getLogger(type(self).__name__)

    def format_data_dict(self):
        article_data = []
        if not self.fetched_data:
            raise Exception("There's no data to format or clean.")
        for year in self.fetched_data:
            for month in self.fetched_data[year]:
                if not self.fetched_data[year][month]:
                    self.logger.warning(f"No data exists for {month}, {year}.")
                    continue
                article_data += self.fetched_data[year][month]

        self.fetched_data = article_data
        self.build_clean_dict()

    def build_clean_dict(self):
        for article in self.fetched_data:
            date = article["pub_date"]
            regex_capture = re.search(r"(\d{4})-",date).group(1)
            if regex_capture in self.cleaned_data:
                if date in self.cleaned_data[regex_capture]:
                    self.cleaned_data[regex_capture][date + article["headline"]["main"][:8]] = article # added the last indexing to shorten publication date name when duplicate
                else:
                    self.cleaned_data[regex_capture][date] = article

            else:
                self.cleaned_data[regex_capture] = {}
                self.cleaned_data[regex_capture][date] = article


    def convert_to_dataframe(self):
        if not self.cleaned_data: raise Exception("Must first call on .clean_data() before converting to dataframe.")

        self.cleaned_data = pd.DataFrame.from_dict({(i, j): self.cleaned_data[i][j]
                                              for i in self.cleaned_data.keys()
                                              for j in self.cleaned_data[i].keys()},
                                             orient='index')

        self.cleaned_data = self.cleaned_data.rename_axis(['Year', 'Publication Date']).sort_index()

        pub_date = self.cleaned_data["pub_date"].str.split("-", expand=True)
        pub_date.drop([2], axis=1, inplace=True)
        pub_date.columns = ["Year", "Month"]
        pub_date['Month Published'] = pub_date["Month"].apply(self.date_cleaning)

        self.cleaned_data["Year Column"], self.cleaned_data["Month"], self.cleaned_data["Month Numeric"] = pub_date.values.T
        self.cleaned_data['subject'] = self.cleaned_data['keywords'].apply(CleanData.subject_cleaning)
        self.cleaned_data['main_line'] = self.cleaned_data['headline'].apply(CleanData.headline_main_cleaning)
        self.cleaned_data['print_headline'] = self.cleaned_data['headline'].apply(CleanData.headline_print_line_cleaning)
        self.cleaned_data['web_url'] = self.cleaned_data['web_url'].apply(CleanData.link_formatting)

    def save_cleaned_data(self, START_YEAR, END_YEAR):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"Article_Data_Cleaned_Df_({START_YEAR}-{END_YEAR}).json")
        if self.cleaned_data.empty:
            raise Exception("There is no data to save must call on .clean_data() method before saving.")
        self.cleaned_data.to_json(file_path)
    
    def reload_cleaned_data(self, START_YEAR, END_YEAR):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"Article_Data_Cleaned_Df_({START_YEAR}-{END_YEAR}).json")
        self.cleaned_data = pd.read_json(file_path)

    def get_cleaned_data(self):
        return self.cleaned_data
    
    @staticmethod
    def date_cleaning(value):
        month_dictionary = {'01': 'January', '02': 'Feburary', '03': 'March', '04': 'April', '05': 'May',
                            '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October',
                            '11': 'November', '12': 'December'}
        return month_dictionary[value]

    @staticmethod
    def subject_cleaning(alist):
        if alist:
            return str([adict['value'] for adict in alist if adict['name'] == 'subject'])

    @staticmethod
    def headline_main_cleaning(adict):
        if adict:
            return adict['main']

    @staticmethod   
    def headline_print_line_cleaning(adict):
        if adict:
            return adict['print_headline']

    @staticmethod        
    def link_formatting(link):
        return f"[Article Link]({link})"
    





























# ----- Ignore -------- #
    
    # def convert_to_dataframe(self):
    #     if self.cleaned_data == None: raise Exception("Must first call on .clean_data() before converting to dataframe.")

    #     self.cleaned_data = pd.DataFrame.from_dict({(i, j): self.cleaned_data[i][j]
    #                                           for i in self.cleaned_data.keys()
    #                                           for j in self.cleaned_data[i].keys()},
    #                                          orient='index')

    #     self.cleaned_data = self.cleaned_data.rename_axis(['Year', 'Publication Date']).sort_index()

    #     pub_date = self.cleaned_data["pub_date"].str.split("-", expand=True)
    #     pub_date.drop([2], axis=1, inplace=True)
    #     pub_date.columns = ["Year", "Month"]

    #     def date_cleaning(value):
    #         month_dictionary = {'01': 'January', '02': 'Feburary', '03': 'March', '04': 'April', '05': 'May',
    #                             '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October',
    #                             '11': 'November', '12': 'December'}
    #         return month_dictionary[value]

    #     pub_date['Month Published'] = pub_date["Month"].apply(date_cleaning)

    #     self.cleaned_data["Year Column"], self.cleaned_data["Month"], self.cleaned_data["Month Numeric"] = pub_date.values.T

    #     def subject_cleaning(alist):
    #         if alist:
    #             return str([adict['value'] for adict in alist if adict['name'] == 'subject'])

    #     self.cleaned_data['subject'] = self.cleaned_data['keywords'].apply(subject_cleaning)

    #     def headline_main_cleaning(adict):
    #         if adict:
    #             return adict['main']

    #     self.cleaned_data['main_line'] = self.cleaned_data['headline'].apply(headline_main_cleaning)

    #     def headline_print_line_cleaning(adict):
    #         if adict:
    #             return adict['print_headline']

    #     self.cleaned_data['print_headline'] = self.cleaned_data['headline'].apply(headline_print_line_cleaning)

    #     def link_formatting(link):
    #         return f"[Article Link]({link})"

    #     self.cleaned_data['web_url'] = self.cleaned_data['web_url'].apply(link_formatting)