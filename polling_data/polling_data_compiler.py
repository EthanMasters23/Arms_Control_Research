from pprint import pprint
import pandas as pd
import re
import plotly.express as px
import os


class PollingDataCompiler:
    def __init__(self, FILE):
        self.polling_data = pd.read_csv(FILE)

    def run_main(self):
        self.isolate_surveys()
        self.save_polling_data()
        self.data_visualization()

    def run_reload(self):
        self.reload_polling_data()
        self.data_visualization()
    
    def isolate_surveys(self):
        self.polling_data['year'] = self.polling_data.BegDate.apply(self.clean_date)
        self.polling_data.drop_duplicates(subset = ["BegDate","EndDate","SampleSize"], keep='first') 

    def data_visualization(self):
        self.polling_data = self.polling_data.groupby(["year"]).size().reset_index()
        self.polling_data.columns = ['year','count']
        px.bar(self.polling_data,x="year", y="count",title=f"Polling Data over the years",labels={"variable":"Key"}).show()

    def save_polling_data(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', "PollingData.csv")
        self.polling_data.to_csv(file_path)

    def reload_polling_data(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', "PollingData.csv")
        self.polling_data = pd.read_csv(file_path)

    @staticmethod
    def clean_date(date):
        return int(re.search(r'\d*/\d*/(\d{4})',date).group(1))


if __name__ == "__main__":
    caller = PollingDataCompiler(
        FILE = os.path.join(os.path.dirname(__file__), '..', 'assets', "roper-folder-toplines-asof-20230127.csv")
    )
    caller.run_reload()
