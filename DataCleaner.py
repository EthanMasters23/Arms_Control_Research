import pandas as pd
import re

class CleanData:
    def __init__(self, input_data):
        self.input_data = input_data
        self.cleaned_dict = None
        self.cleaned_data = None

    def clean_data(self):
        data = self.input_data
        processed_dict = {}

        for year in data:
            for month in data[year]:
                if not data[year][month]:
                    print(f"No data exists for {month}, {year}.")
                    continue
                for article in data[year][month]:
                    date = article["pub_date"]
                    if re.search(r"(\d{4})-",article["pub_date"]).group(1) in processed_dict:
                        if article["pub_date"] in processed_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)]:
                            processed_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)][date + article["headline"]["main"][:8]] = article # added the last indexing to shorten publication date name when duplicate
                        else:
                            processed_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)][date] = article

                    else:
                        processed_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)] = {}
                        processed_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)][date] = article

        self.cleaned_dict = processed_dict

    def convert_to_dataframe(self):
        if self.cleaned_dict == None: raise Exception("Must first call on .clean_data() before converting to dataframe.")

        output_data = pd.DataFrame.from_dict({(i, j): self.cleaned_dict[i][j]
                                              for i in self.cleaned_dict.keys()
                                              for j in self.cleaned_dict[i].keys()},
                                             orient='index')

        final_output = output_data.rename_axis(['Year', 'Publication Date']).sort_index()

        pub_date = final_output["pub_date"].str.split("-", expand=True)
        pub_date.drop([2], axis=1, inplace=True)
        pub_date.columns = ["Year", "Month"]

        def date_cleaning(value):
            month_dictionary = {'01': 'January', '02': 'Feburary', '03': 'March', '04': 'April', '05': 'May',
                                '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October',
                                '11': 'November', '12': 'December'}
            return month_dictionary[value]

        pub_date['Month Published'] = pub_date["Month"].apply(date_cleaning)

        final_output["Year Column"], final_output["Month"], final_output["Month Numeric"] = pub_date.values.T

        def subject_cleaning(alist):
            if alist:
                return str([adict['value'] for adict in alist if adict['name'] == 'subject'])

        final_output['subject'] = final_output['keywords'].apply(subject_cleaning)

        def headline_main_cleaning(adict):
            if adict:
                return adict['main']

        final_output['main_line'] = final_output['headline'].apply(headline_main_cleaning)

        def headline_print_line_cleaning(adict):
            if adict:
                return adict['print_headline']

        final_output['print_headline'] = final_output['headline'].apply(headline_print_line_cleaning)

        def link_formatting(link):
            return f"[Article Link]({link})"

        final_output['web_url'] = final_output['web_url'].apply(link_formatting)

        self.cleaned_data = final_output

    def save_data(self, filename):
        if self.cleaned_data == None: raise Exception("There is no data to save must call on .clean_data() method before saving.")
        self.cleaned_data.to_json(filename)

    def get_data(self):
        return self.input_data

    def get_cleaned_data(self):
        return self.cleaned_data