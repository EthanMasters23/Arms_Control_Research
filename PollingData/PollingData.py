from pprint import pprint
import pandas as pd
import re
import plotly.express as px
import os
import threading
import queue

from datetime import datetime

class PollingData:
    def __init__(self):
        self.polling_data = pd.read_csv("src/roper-folder-toplines-asof-20230127.csv")

    def run(self):
        self.polling_data['year'] = self.polling_data.BegDate.apply(self.clean_date)
        self.isolate_surveys()
        self.data_visualization()
    
    def isolate_surveys(self):
        self.polling_data.drop_duplicates(subset = ["BegDate","EndDate","SampleSize"], keep='first') 

    def data_visualization(self):
        self.polling_data = self.polling_data.groupby(["year"]).size().reset_index()
        self.polling_data.columns = ['year','count']
        px.bar(self.polling_data,x="year", y="count",title=f"Polling Data over the years",labels={"variable":"Key"}).show()

    def save_polling_data(self):
        self.polling_data.to_csv("assets/PollingData.csv")

    
    @staticmethod
    def clean_date(date):
        return int(re.search(r'\d*/\d*/(\d{4})',date).group(1))

class Worker(threading.Thread):
    def __init__(self, q, lock):
        self.q = q
        self.lock = lock
        super().__init__()

    def run(self):
        while True:
            try:
                work = self.q.get(timeout=3)
            except queue.Empty:
                return
            
            cwd = os.getcwd()
            datapath = cwd + "/assets/"
            file = work + '.csv'
            df = pd.read_csv(datapath + "/" + file)
            self.lock.acquire()
            print('Starting' + work)
            self.lock.release()
            PollingData(df).run()
            self.lock.acquire()
            print('Completed cleaning' + work)
            self.lock.release()

            self.q.task_done()

if __name__ == "__main__":
    q = queue.Queue()

    q.put_nowait('roper-folder-toplines-asof-20230127')

    starttime = datetime.now()

    lock = threading.Lock()

    for _ in range(1): # changed range from 2
        Worker(q,lock).start()
    q.join()