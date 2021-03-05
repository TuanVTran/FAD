import constant.configuration as constant
from utils import utilities as utils
from calculator.fad_calculator import *
import pandas as pd
import datetime as dt
import numpy as np
import decimal
from os import path

class BenchmarkReturn():
    def __init__(self):
        
        self.crbm_df = None
        self.benchmark_input_df = self.get_benchmark_input_from_file()
        self.benchmark_return_df = self.get_benchmark_return_from_file()
        self.calculate_benchmark_return()

    def get_benchmark_input_from_file(self):

        dir_path = utils.get_data_sample_dir_path()
        fund_df = pd.read_csv(dir_path + 'MgrBenchInput.csv', 
                            index_col=None)

        return fund_df

    def get_benchmark_return_from_file(self):

        dir_path = utils.get_data_sample_dir_path()
        fund_df = pd.read_csv(dir_path + 'BBGReturnMnth.csv', 
                            index_col=None, parse_dates=['Date'])
        return fund_df

    # get from file or cache if calculated , if not we calculate and save
    def calculate_benchmark_return(self):
        dir_path = utils.get_data_sample_dir_path()
        if path.exists(dir_path + 'crmb.csv'):
            custom_date_parser = lambda x: dt.datetime.strptime(x, "%m/%d/%Y")
            self.crbm_df = pd.read_csv(dir_path + 'crmb.csv',
                            index_col=None, parse_dates=['Date'])
        else:
            # read calculate from two dataframe
            pass

    def get_bechmark_return_by_acc(self, acc, from_date):
        mask = (self.crbm_df['Account'] == acc) & (self.crbm_df['Date'] >= from_date)
        return self.crbm_df[mask]
    
    def get_bechmark_return_by_acc_date(self, acc, date):
        mask = (self.crbm_df['Account'] == acc) & (self.crbm_df['Date'] == date)
        try:
            benchmark = self.crbm_df[mask].iloc[0]['CRBM']
            return benchmark
        except:
            return 0


        
        
        




    