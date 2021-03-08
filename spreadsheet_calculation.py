import pandas as pd
import datetime as dt
import time
import numpy as np
import sys
import pandas_datareader as pdr

from calculator.fad_calculator import *
from spread_model.fund_nav_model import FundNAV
from spread_model.model_management import ModelManagement
from spread_model.benchmark_model import BenchmarkReturn
from spread_model.trans_model import Transaction

def get_sp500(start_date, end_date):
    try:
        sp500_all_data = pdr.get_data_yahoo("SPY", start_date, end_date)
    except ValueError:
        print("ValueError, trying again")
    sp500_data = sp500_all_data["Adj Close"]

    sp500_data_df = pd.DataFrame({'Date': sp500_all_data.index.values, 'SP500': sp500_data.values}, columns=['Date', 'SP500'])
    return sp500_data_df

def export_report_with_spreadsheet_data():

    # get ten year sp500 data
    end_date = dt.datetime.now()
    start_date = dt.datetime(end_date.year - 10, end_date.month, end_date.day)
    sp500_benchmark_df = get_sp500(start_date, end_date)
    
    ModelManagement().add_benchmark_model(BenchmarkReturn())
    ModelManagement().add_transaction_model(Transaction())
    ModelManagement().add_fund_nav_model(FundNAV())

    nav = ModelManagement().fund_nav_model
    nav.calculate_nav_data()
    nav.export_nav_cal()
    nav.calculate_fund_ratios(sp500_benchmark_df)
    nav.export_ratios()