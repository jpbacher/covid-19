import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import requests
import time
import datetime
from datetime import date


class Covid:
    def __init__(self):
        self.state = None
        self.county = None
        self._state_updated = False
        self._county_updated = False
        self._is_processed = False
        self._date_today = self._get_date_today()

    def _get_date_today(self):
        text = f"Today's date: {date.today()}"
        return text

    def update_state(self, url="https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"):
        content = requests.get(url).content
        self.state = pd.read_csv(io.StringIO(content.decode('utf-8')))
        self.state['date'] = pd.to_datetime(self.state['date'], format='%Y-%m-%d')
        self._state_updated = True


    def update_county(self, url="https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"):
        content =  requests.get(url).content
        self.county = pd.read_csv(io.StringIO(content.decode('utf-8')))
        self.county['date'] = pd.to_datetime(self.state['date'], format='%Y-%m-%d')
        self._county_updated = True

    def quick_look(self):
        if self._state_updated:
            print('first five rows of state-wide data:')
            print('*' * 30)
            print(self.state.head())
        if self._county_updated:
            print('first five rows of county data')
            print('*' * 30)
            print(self.county.head())

    def process_data(self):
        self.state_dict = {}
        self.county_dict = {}
        print('processing data......')
        start = time.time()
        if self._state_updated:
            self.state_list = list(self.state['state'].unique())
            for s in self.state_list:
                state_df = self.state.loc[self.state['state'] == s]
                state_df['new_cases'] = state_df['cases'].diff()
                state_df['new_deaths'] = state_df['deaths'].diff()
                self.state_dict = state_df
        if self._county_updated:
            self.county_list = list(self.county['county'].unique())
            for c in self.county_list:
                county_df = self.county.loc[self.county['county'] == c]
                county_df['new_cases'] = county_df['cases'].diff()
                county_df['new_deaths'] = county_df['deaths'].diff()
                self.county_dict = county_df
        self._is_processed = True
        end = time.time()
        print(f'completed, total time: {end - start} seconds')

    def plot_state(self, state='Georgia', last_30_days=False):
        if not self._is_processed:
            print('Data not processed')
        assert state in self.state_list, 'state not in list of states'

        df = self.state_dict[state]
        dates = df['date']
        cases = df['cases']
        deaths = df['deaths']
        new_cases = df['new_cases']
        new_deaths = df['new_deaths']

        if last_30_days:
            dates = df['date'][-31: -1]
            cases = df['cases'][-31: -1]
            deaths = df['deaths'][-31: -1]
            new_cases = df['new_cases'][-31: -1]
            new_deaths = df['new_deaths'][-31: -1]

        plt.figure(figsize=(15, 6))
        if last_30_days:
            plt.title(f'Cumulative Covid Cases for {state} in Last 30 Days')
        else:
            plt.title(f'Cumulative Covid Cases for {state}')
        plt.bar(x=dates, height=cases, color='red', edgecolor='k')
        plt.xticks(rotation=45, fontsize=9)
        sns.despine(left=True)
        plt.show()
        print('\n')

        plt.figure(figsize=(15, 6))
        if last_30_days:
            plt.title(f'Cumulative Covid Deaths for {state} in Last 30 Days')
        else:
            plt.title(f'Cumulative Covid Deaths for {state}')
        plt.bar(x=dates, height=deaths, color='blue', edgecolor='k')
        plt.xticks(rotation=45, fontsize=9)
        sns.despine(left=True)
        plt.show()
        print('\n')

        plt.figure(figsize=(15, 6))
        if last_30_days:
            plt.title(f'New Covid Cases for {state} in Last 30 Days')
        else:
            plt.title(f'New Covid Cases for {state}')
        plt.bar(x=dates, height=new_cases, color='red', edgecolor='k')
        plt.xticks(rotation=45, fontsize=9)
        sns.despine(left=True)
        plt.show()
        print('\n')

        plt.figure(figsize=(15, 6))
        if last_30_days:
            plt.title(f'New Covid Deaths for {state} in Last 30 Days')
        else:
            plt.title(f'New Covid Deaths for {state}')
        plt.bar(x=dates, height=new_deaths, color='red', edgecolor='k')
        plt.xticks(rotation=45, fontsize=9)
        sns.despine(left=True)
        plt.show()
        print('\n')













