import requests
import pickle
import pandas as pd
from pprint import pprint
import time
from datetime import datetime

def get_article_count(api_key):
    article_count = {}

    for year in range(1945, 2024):
        start = f'{year}0101'
        end = f'{year}1231'
        request_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={start}&end_date={end}&sort=newest&api-key={api_key}"

        try:
            response = requests.get(request_url)
            response.raise_for_status()
            response_data = response.json()["response"]
            article_count[year] = response_data['meta']['hits']
        except requests.exceptions.HTTPError as ERROR:
            if response.status_code == 401:
                print("Unauthorized request. Make sure api-key is set.")
            elif response.status_code == 429:
                print("Too many requests. You reached your per minute or per day rate limit.")
            else:
                print(f"HTTP error occurred: {ERROR}")
        except Exception as ERROR:
            print(f"Error{time.time}: {ERROR}")

        response = requests.get(request_url).json()["response"]
        article_count[year] = response['meta']['hits']

        time.sleep(2)

        pprint(year)

    return article_count

def save_article_total(article_count, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(article_count, f)

def load_articles_total(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)

def to_dataframe(article_count):
    return pd.DataFrame.from_dict(article_count, orient='index')

def to_json(dataframe, json_file_path):
    dataframe.to_json(json_file_path)

def execute():
    api_key = "NNEVLqcrq6X3waJNf0IixwUaerowCqeR"
    article_count_file = "yeardata.pkl"
    json_file_path = "./assets/annual_article_count.json"

    input_response = input("Do you want to use existing saved data? (y/n): ").lower() == 'y'

    if input_response:
        try:
            article_count = load_articles_total(article_count_file)
        except FileNotFoundError:
            print("No article data found. Starting article data fetching...")
            input_response = False

    if not input_response:
        print("Starting article data fetching...")
        article_count = get_article_count(api_key)
        save_article_total(article_count, article_count_file)

    df = to_dataframe(article_count)
    to_json(df, json_file_path)

    pprint(df)

    pprint(df.describe())

if __name__ == "__main__":
    execute()


