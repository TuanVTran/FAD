import constant.file_name as file_cst
import fad_utilities as fad_utils
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
        self.bbg_return_df = self.get_bbg_return_from_file()
        self.get_benchmark_return()

    def get_benchmark_input_from_file(self):

        dir_path = fad_utils.get_data_sample_dir_path()
        fund_df = pd.read_csv(dir_path + 'MgrBenchInput.csv', 
                            index_col=None)

        return fund_df

    def get_bbg_return_from_file(self):

        dir_path = fad_utils.get_data_sample_dir_path()
        fund_df = pd.read_csv(dir_path + 'BBGReturnMnth.csv', 
                            index_col=None, parse_dates=['Date'])
        return fund_df

    # get from file or cache if calculated , if not we calculate and save
    def get_benchmark_return(self):
        dir_path = fad_utils.get_data_sample_dir_path()
        if path.exists(dir_path + 'crbm.csv'):
            self.crbm_df = pd.read_csv(dir_path + 'crbm.csv',
                            index_col=None, parse_dates=['Date'])
        else:
            # read calculate from two dataframe
            self.crbm_df = self.calculate_benchmark_return()

    def get_bechmark_return_by_acc(self, acc_num, acc_name, from_date):
        try:
            acc_benchmark = self.crbm_df[['Date', acc_num]]
            acc_benchmark = acc_benchmark[acc_benchmark['Date'] >= from_date]
            acc_benchmark['CRBM'] = acc_benchmark[acc_num]
            acc_benchmark['CRBM'] = acc_benchmark['CRBM']
            return acc_benchmark
        except:
            return None
    
    def get_bechmark_return_in_range_date(self, acc_num, acc_name, list_date):
        try:
            acc_benchmark = self.crbm_df[['Date', acc_num]]
            acc_benchmark = acc_benchmark[acc_benchmark['Date'].isin(list_date)]
            acc_benchmark['CRBM'] = acc_benchmark[acc_num]
            acc_benchmark['CRBM'] = acc_benchmark['CRBM']
            return acc_benchmark
        except:
            return None

    def get_date_list_in_benchmark(self, from_date):
        acc_benchmark_date = self.crbm_df[self.crbm_df['Date'] >= from_date]['Date']
        return acc_benchmark_date

    def get_bechmark_return_by_acc_date(self, acc_num, acc_name, date):
        try:
            acc_benchmark = self.crbm_df[['Date', acc_num]]
            acc_benchmark = acc_benchmark[acc_benchmark['Date'] == date]
            benchmark = acc_benchmark.iloc[0][acc_num]
            return benchmark
        except:
            return 0
    
    def calculate_benchmark_return(self):
        benchmark_input_df = self.benchmark_input_df
        benchmark_input_df = benchmark_input_df.loc[:, ~benchmark_input_df.columns.str.contains('^Unnamed')]
        benchmark_input_df = benchmark_input_df[(benchmark_input_df['Category'] == 'Beta Adj Exposure') & (benchmark_input_df['Account #'].notna())]
        benchmark_input_df = benchmark_input_df.set_index(['Account #', 'Manager'])
        benchmark_input_df = benchmark_input_df.drop(['AC', 'NAV ($M)', 'Total Exposure', 'Category'], axis=1)

        bbg_return_df = self.bbg_return_df
        bbg_return_df = bbg_return_df.fillna(0)

        cal_benchmark = bbg_return_df.copy()
        cal_benchmark = cal_benchmark.set_index('Date')
        
        bm_cal_return_df = pd.DataFrame([], columns=['Date'])
        bm_cal_return_df['Date'] = bbg_return_df['Date'].to_numpy()
        
        for k,v in benchmark_input_df.iterrows():
            acc_num = k[0]
            x =  cal_benchmark.mul(v.array).sum(axis=1)
            bm_cal_return_df[acc_num] = x.to_numpy()

        dir_path = fad_utils.get_data_sample_dir_path()
        bm_cal_return_df.to_csv(dir_path + 'crbm.csv',index=False)
        return bm_cal_return_df
        
        
        




    