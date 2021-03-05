import constant.configuration as constant
from utils import utilities as utils
from calculator.fad_calculator import *
import pandas as pd
import datetime as dt
import numpy as np
import decimal
D = decimal.Decimal

class Transaction():
    def __init__(self):
        self.date_columns = ['Trade Date', 'Reported Date', 'Posted Date', 
                            'Effective Date', 'Actual Settle Date', 'Contract Settle Date', 
                            'Selection Date', 'Begin Date', 'End Date', 'Report Run Date']

        self.dtype = {'Base Txn Amount': np.float64, 'Base Cost': np.float64}

        self.trans_df = self.get_data_from_file()

    def get_data_from_file(self):

        dir_path = utils.get_data_sample_dir_path()
        fund_df = pd.read_csv(dir_path + constant.TRANSACTION_FILE, 
                            index_col=None, parse_dates=self.date_columns, 
                            converters={'Base Txn Amount': utils.currency_converter, 'Base Cost': utils.currency_converter})
        return fund_df

    def get_transaction(self, report_acc_number, source_acc_number, start_date, end_date):
        columns_filters = ['Reporting Account Number', 'Reporting Account Name', 'Source Account Number', 
                            'Source Account Name', 'Trade Date', 'Effective Date', 'Base Txn Amount', 'Base Cost']

        trans_df = self.trans_df[columns_filters]
        mask =  (trans_df['Reporting Account Number'] == report_acc_number) & \
                (trans_df['Source Account Number'] == source_acc_number) & \
                (trans_df['Effective Date'] > start_date) & \
                (trans_df['Effective Date'] < end_date)

        trans_df = trans_df[mask]
        return trans_df
    
    def get_total_base_txn_amount(self, trans_df):
        return trans_df['Base Txn Amount'].dropna().sum()
        





    