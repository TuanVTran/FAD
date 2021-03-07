
import constant.configuration as constant
import utils.utilities as utils
import pandas as pd
from calculator.fad_calculator import *
import datetime as dt
from spread_model.trans_model import Transaction 
from spread_model.benchmark_model import BenchmarkReturn 
from pandas.tseries.offsets import MonthEnd, MonthBegin

ROLLING_DATA = 12

class FundNAV():
    def __init__(self):
        self.date_columns = ['As Of Date', 'Begin Date']
        self.fund_df = self.get_data_from_file()
        self.fund_ratios_df = None
        self.nav_data = None
        self.benchmark = BenchmarkReturn()
        self.trans = Transaction()

    def get_data_from_file(self):
        dir_path = utils.get_data_sample_dir_path()
        fund_df = pd.read_csv(dir_path + constant.FUND_NAV_FILE, index_col=None, parse_dates=self.date_columns, infer_datetime_format=True)
        return fund_df

    def get_beta(self, fund_nav_data_df, benchmark_data):
        benchmark_list =  [tuple(x) for x in benchmark_data.values]
        fund_nav_list =  [tuple(x) for x in fund_nav_data_df.values]

        window = ROLLING_DATA if len(benchmark_list) > 12 else len(benchmark_list) - 1
        fund_beta = get_beta(fund_nav_list, benchmark_list, window)
        return fund_beta

    def get_beta_by_fund_row(self, fund_row, sp500_df, list_date):

        source_acc_num = fund_row['Source Account Number']
        source_acc_name = fund_row['Source Account Name']

        benchmark_return_df = self.benchmark.get_bechmark_return_in_range_date(source_acc_num, source_acc_name, list_date)

        fund_beta = ''
        if benchmark_return_df is None or benchmark_return_df.empty:
            fund_beta = 'Not have CRBM'
        else:

            benchmark_return_df['nav'] = benchmark_return_df['CRBM'].cumprod()
            fund_nav_data_df = pd.DataFrame({
                'date': list_date.to_numpy(),
                'nav': benchmark_return_df['nav'].to_numpy()
            })

            sp_benchmark_custom_df = pd.DataFrame({
                'date': list_date.to_numpy(),
                'nav': sp500_df['SP500'].to_numpy()
            })
            
            fund_beta = self.get_beta(fund_nav_data_df, sp_benchmark_custom_df)
        return fund_beta

    def calculate_fund_ratios(self, sp500_df):
        def get_sp500_data_by_date(source_date_data):
            working_date_list = []
            for date in source_date_data:
                working_date = date
                if date.day_of_week >= 5:
                    working_date = date - dt.timedelta(date.day_of_week - 4)

                while sp500_df[sp500_df['Date'] == working_date].empty :
                    working_date = working_date - dt.timedelta(1)

                working_date_list.append(working_date)
            return sp500_df[sp500_df['Date'].isin(working_date_list)]

        columns_filters = ['Reporting Account Number', 'Reporting Account Name', 'Source Account Number', 
                            'Source Account Name', 'Begin Date']

        fund_filter_fd = self.fund_df[columns_filters]
        self.fund_ratios_df = fund_filter_fd.groupby(['Reporting Account Number', 'Source Account Number']).first().reset_index()

        start_sp500_date = sp500_df.iloc[0]['Date']
        benchmark_list_date = self.benchmark.get_date_list_in_benchmark(start_sp500_date)
        sp5000_index_by_date_df = get_sp500_data_by_date(benchmark_list_date)
        self.fund_ratios_df['Beta'] = self.fund_ratios_df.apply(lambda row: self.get_beta_by_fund_row(row, sp5000_index_by_date_df, benchmark_list_date), axis=1)

    def export_ratios(self):
        dir_path = utils.get_data_sample_dir_path()
        self.fund_ratios_df.to_csv(dir_path + constant.FUND_RATIOS_FILE, index=False)

    def export_nav_cal(self, nav_df = None):
        export_nav = nav_df
        if nav_df is None:
            export_nav = self.nav_data

        dir_path = utils.get_data_sample_dir_path()
        export_nav.to_csv(dir_path + constant.FUND_NAV_CAL_FILE, index=False)

    def get_begin_nav_by_group(self, fund_fd):
        fund_grouped_by_report = fund_fd.groupby(['Reporting Account Number', 'As Of Date']).sum() \
                                                    .groupby(level=0).cumsum().reset_index()
        return fund_grouped_by_report

    def get_end_nav(self, fund_row):

        transaction_df = self.trans.get_transaction(fund_row['Reporting Account Number'], fund_row['Source Account Number'], fund_row['As Of Date'], fund_row['End Date'])
        transaction_df['date'] = transaction_df['Effective Date']
        transaction_df['value'] = transaction_df['Base Txn Amount']
        return get_end_nav(fund_row['Total Market Value'], fund_row['BM'], transaction_df, fund_row['As Of Date'], fund_row['End Date'])

    def calculate_nav_data(self):
        columns_filters = ['Reporting Account Number', 'Reporting Account Name', 'Source Account Number', 
                            'Source Account Name', 'Begin Date', 'As Of Date', 'Total Market Value']

        self.nav_data = self.fund_df[columns_filters]
        self.nav_data = self.nav_data[self.nav_data.groupby(['Reporting Account Number', 'Source Account Number'])['As Of Date'].transform('max') == self.nav_data['As Of Date']]
      
        self.nav_data['End Date'] = pd.to_datetime(self.nav_data['As Of Date']) + MonthEnd(1)
        self.nav_data['BM'] = self.nav_data.apply(lambda row: self.benchmark.get_bechmark_return_by_acc_date(row['Source Account Number'], row['Source Account Name'], row['End Date']), axis=1)
        self.nav_data['End NAV'] = self.nav_data.apply(lambda row: self.get_end_nav(row), axis=1)
        self.nav_data['ROR'] = (self.nav_data['End NAV'] - self.nav_data['Total Market Value'])/self.nav_data['Total Market Value']
