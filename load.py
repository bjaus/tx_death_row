#!/bin/python

import os, sys, re
from glob import glob
from subprocess import call
from argparse import ArgumentParser
from datetime import date, time, datetime, timedelta
from cdecimal import Decimal
# import googlemaps

from selenium import webdriver
from selenium.webdriver.support.ui import Select

import pandas as pd
import numpy as np

# from info import GOOGLE_MAPS_KEY

pd.options.display.max_columns = 35
pd.options.display.max_rows = 100

# -------------------------------------------------------------------------------------------------


class DeathRowLoader(object):

    def __init__(self):
        self.driver = self._homepage()

        self.df = self.load_offenders_on_death_row()


    def _homepage(self):
        url = 'https://www.tdcj.state.tx.us/death_row/index.html'
        driver = webdriver.Chrome('./chromedriver')
        driver.get(url)
        return driver



    def load_offenders_on_death_row(self):
        data = list()

        tag_name = self.driver.find_elements_by_tag_name
        self.driver.find_elements_by_tag_name('ul')[1]\
                   .find_elements_by_tag_name('li')[0]\
                   .find_element_by_tag_name('a')\
                   .click()
        
        table = self.driver.find_elements_by_tag_name('tr')
        for tr in table:
            tds = tr.find_elements_by_tag_name('td')
            record = list()
            for n, td in enumerate(tds):
                text = td.text
                if n != 1:
                    record.append(text)
            data.append(record)
        cols = ['tdcj_num', 'last_name', 'first_name', 'dob', 'sex', 'race', 'date_received', 'county', 'date_of_offense']
        return pd.DataFrame(data, columns=cols)



def date_converter(item):
    if item:
        i = item.split('/')
        if len(i) == 3:
            m, d, y = tuple(i)
        elif len(i) == 2:
            m, y = tuple(i)
            d = '1'
        else:
            return pd.NaT
        if len(y) == 2:
            y = '19' + y
        m, d, y = int(m), int(d), int(y)
        return datetime(y, m, d)
    return pd.NaT


def get_age(item):
    if item.year:
        return datetime.now().year - item.year
    else:
        return np.nan


def free_days(item):
    if item:
        return item.days
    return np.nan

def free_years(item):


def main():
    dr = DeathRowLoader()
    dr.driver.close()


if __name__ == '__main__':
    from time import sleep
    main()



COLUMNS = [
    'tdcj_num',
    'last_name',
    'first_name',
    'dob',
    'gender',
    'race',
    'date_received',
    'county',
    'date_of_offense',
    'fullname',
    'age_received',
    'education_level',
    'age_time_of_offense',
    'hair_color',
    'height',
    'weight',
    'eye_color',
    'native_county',
    'native_state',
    'prior_occupation',
    'prior_prison_record',
    'summary_of_incident',
    'co_defendants',
    'race_gender_of_victim'
]