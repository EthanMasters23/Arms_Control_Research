import pandas as pd
import plotly.express as px

class DataGrapher:
    def __init__(self, input_data):
        self.input_df = input_data

    def group_by_year(self):
        self.input_df = pd.DataFrame(self.input_df.groupby(level=['Year']).size()).reset_index()
        self.input_df.columns = ["Year","Article Count"]

    def plot_time_series(self):
        template = "plotly_dark"
        fig = px.bar(self.input_df, x = "Year", y = "Article Count",
                    title = f"Time Series Data Articles/Year",
                    labels = {"variable": "Key"},
                    template = template)
        fig.show()