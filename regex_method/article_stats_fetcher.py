from tqdm import tqdm
import requests
import pandas as pd
import time
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
import os


class FetchArticleStats:
    def __init__(self, apiKey, startYear, endYear):
            self.API_KEY = apiKey
            self.START_YEAR = startYear
            self.END_YEAR = endYear

            self.article_stats = {
                              'print_page' : {},
                              'news_desk' : {},
                              'keywords' : {},
                              'section_name' : {},
                              'document_type' : {},
                              'type_of_material' : {},
                              'keywords' : {}
                              }

    def get_article_stats(self):
        for year in tqdm(range(self.START_YEAR, self.END_YEAR + 1)):
            print(f"Starting article stats collection for {year}...")

            for key in self.article_stats.keys():
                self.article_stats[key][year] = {}

            for month in tqdm(range(1, 13)):
                response = requests.get(f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={self.API_KEY}')

                if response.status_code == 200: response = response.json()
                elif response.status_code == 401: raise Exception("Unauthorized request, check api-key is set.")
                elif response.status_code == 429: raise Exception("Too many requests. Reached your per minute or per day rate limit.")
                else: raise Exception("An error occurred:", response.status_code)

                for article in response["response"]["docs"]: 
                    for key in self.article_stats.keys():
                        if key in article.keys(): 
                            if key != 'keywords':
                                if article[key] in self.article_stats[key][year].keys(): self.article_stats[key][year][article[key]] += 1
                                else: self.article_stats[key][year][article[key]] = 1
                            else:
                                for item in article[key]:
                                        if item['value'] in self.article_stats[key][year].keys() : self.article_stats[key][year][item['value']] += 1
                                        else: self.article_stats[key][year][item['value']] = 1

                time.sleep(2)
            print(f"Finished collecting article stats from {year}.")
        print("\n"*5)

    def convert_dict_to_decades(self):
        decade_dict = {}
        for keys, values in self.article_stats.items():
            decade_dict[keys] = {}
            i = 0
            for key, value in values.items():
                if i > 10:
                    break
                decade_dict[keys][key] = value
                if 'None' in decade_dict[keys][key].keys():
                    decade_dict[keys][key].pop('None')
                i += 1

        return decade_dict

    def view_article_stats(self):
        reloaded_data = self.convert_dict_to_decades()

        for data_dict, title in [(reloaded_data['keywords'], 'Keywords'), (reloaded_data['print_page'], 'Print Pages'),
                             (reloaded_data['news_desk'], 'News Desks'), (reloaded_data['section_name'], 'Section Names'),
                             (reloaded_data['document_type'], 'Document Types'), (reloaded_data['type_of_material'], 'Material Types')]:
            fig = make_subplots(rows=1, cols=len(data_dict), subplot_titles=list(data_dict.keys()))

            for i, (year, data) in enumerate(data_dict.items()):
                df = pd.DataFrame.from_dict({year: data}, orient='index')
                fig.add_trace(go.Bar(x=df.columns, y=df.values.flatten(), name=year), row=1, col=i+1)

                fig.update_layout(title=title, showlegend=False)
                fig.update_xaxes(title_text="Year")
                fig.update_yaxes(title_text="Frequency")

            fig.show()

    def save_article_stats(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"NYT_API_Article_Stats_({self.START_YEAR}-{self.END_YEAR}).json")
        with open(file_path, 'w') as file:
            json.dump(self.article_stats, file)

    def reload_article_stats(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"NYT_API_Article_Stats_({self.START_YEAR}-{self.END_YEAR}).json")
        try:
            with open(file_path, 'r') as file:
                self.article_stats = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")