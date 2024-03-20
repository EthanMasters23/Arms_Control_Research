##### Migrate ####
import pandas as pd
import plotly.express as px

def data_visualization(file_name):

    final_regex_output = pd.read_json(f"./assets/{file_name}.json", orient='table')
    article_occurrences_df = pd.DataFrame(final_regex_output.groupby(level=['Year']).size()).reset_index(inplace=True)
    article_occurrences_df.columns = ["Year","Article Count"]
    plot_time_series(article_occurrences_df)

def plot_time_series(df, file_name):
    template = "plotly_dark"
    fig = px.bar(df, x="Year", y="Article Count",
                title=f"Time Series Data Articles/Year File: {file_name}",
                labels={"variable": "Key"},
                template=template)
    fig.show()

if __name__ == '__main__':
    input_file = ("Input File Name: ").strip()
    data_visualization(input_file)


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