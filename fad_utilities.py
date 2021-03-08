import pandas as pd
import datetime as dt
import time
import numpy as np
import os

def to_date(date_str):
    return dt.datetime.strptime(date_str, "%m/%d/%Y").date()

def get_data_dir_path():
    dir_path = os.getcwd()
    return dir_path + "\\data\\"

def get_data_sample_dir_path():
    dir_path = os.getcwd()
    return dir_path + "\\AccountingDataSample\\"

def get_start_next_month(cur_date):
    return (cur_date.replace(day=1) + dt.timedelta(days=32)).replace(day=1)

def get_end_month(cur_date):
    return get_start_next_month(cur_date) - dt.timedelta(1)

def currency_converter(x):
    x = (x.replace( '$','' )
        .replace( '(','-')
        .replace( ')','')
        .replace( ',','' ))
    return float(x)

def format_float_number(x):
    return format(x, '.2f')