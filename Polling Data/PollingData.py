from pprint import pprint
import pandas as pd
import re
import plotly.express as px


class PollingData:
    def __init__(self):
        self.polling_data = pd.read_csv("assets/roper-folder-toplines-asof-20230127.csv")
        self.polling_data['year'] = self.polling_data.BegDate.apply(self.clean_date)

    def run_main(self):
        self.isolate_surveys()
        self.save_polling_data()
        self.data_visualization()

    def run_reload(self):
        self.reload_polling_data()
        self.data_visualization()
    
    def isolate_surveys(self):
        self.polling_data.drop_duplicates(subset = ["BegDate","EndDate","SampleSize"], keep='first') 

    def data_visualization(self):
        self.polling_data = self.polling_data.groupby(["year"]).size().reset_index()
        self.polling_data.columns = ['year','count']
        px.bar(self.polling_data,x="year", y="count",title=f"Polling Data over the years",labels={"variable":"Key"}).show()

    def save_polling_data(self):
        self.polling_data.to_csv("assets/PollingData.csv")

    def reload_polling_data(self):
        self.polling_data = pd.read_csv("assets/PollingData.csv")

    @staticmethod
    def clean_date(date):
        return int(re.search(r'\d*/\d*/(\d{4})',date).group(1))


if __name__ == "__main__":
    caller = PollingData()
    caller.run_reload()
