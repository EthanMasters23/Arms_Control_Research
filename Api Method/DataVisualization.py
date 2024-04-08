##### Migrate ####
import pandas as pd
import plotly.express as px

class DataGrapher:
    def __init__(self, input_data):
        self.input_df = input_data

    def group_by_year(self):
        self.input_df = pd.DataFrame(self.input_df.groupby(level=['Year']).size()).reset_index(inplace=True)
        self.input_df.columns = ["Year","Article Count"]
        self.plot_time_series(self.input_df)

    def plot_time_series(self):
        template = "plotly_dark"
        fig = px.bar(self.input_df, x="Year", y="Article Count",
                    title=f"Time Series Data Articles/Year",
                    labels={"variable": "Key"},
                    template=template)
        fig.show()












################################## - DATA VISUALIZATION FOR ARTCILES BY MONTH - ##################################

# # # print(plt.style.available) (WORKING)
# plt.style.use("dark_background")
# template = "plotly_dark" # LOVE

# df.columns = ["January","Feburary","March","April","May","June","July","August","September","October","November","December"]

# ### - year and month using px- ### (WORKING)

### - line graph - ###
# df=df.applymap(lambda x : int(x["Article Count"]))
# px.line(df,x=df.index, y=df.columns,
#     title="Time Series Data Articles/Year", 
#     labels={"index": "Year", "value": "Articles","variable":"Key"},
#     template=template).show()

# y = df.replace(0, np.nan, inplace=True) # drop zeros after line graph

### - bar chart - ###
# px.bar(df,x=df.index, y=df.columns,
#     title="Time Series Data Articles/Year",
#     labels={"index": "Year", "value": "Articles","variable":"Key"},
#     template=template).show()

### - scatter plot - ###
# px.scatter(df, x=df.index, y=df.columns, 
#     marginal_y="box",
#     title="Time Series Data Articles/Year",
#     labels={"index": "Year", "value": "Articles","variable":"Month"},
#     template=template).show()

# ### - year and month using px (END) - ### (WORKING)

# ############################## - Experimental - #####################################

# ### - HEAT MAP - ### (WORKING)

# plt.title('Average Yearly Article Matches')
# sns.heatmap(df, annot=True, cmap='RdYlBu_r', fmt= '.7g',)
# plt.xlabel('Year-Month')
# plt.ylabel('District')
# plt.show()

# ### - HEAT MAP - ###

### - scatter plot - ###

# plt.plot(np.arange(1945-1945,2022-1945), df.applymap(lambda x : x["Article Count"]).values, 'o',label=df.columns)
# plt.legend()
# plt.title("Time Series Data Articles/Year", fontsize=14)
# plt.xlabel('Year', fontsize=14)
# plt.ylabel("Articles", fontsize=14)
# plt.grid(True)
# mplcursors.cursor(hover=True)

### - scatter plot - ###

################################## - DATA VISUALIZATION FOR ARTCILES BY MONTH (END) - ##################################