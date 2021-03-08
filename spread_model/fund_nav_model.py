
import constant.file_name as file_cst
import fad_utilities as fad_utils
import pandas as pd
from calculator.fad_calculator import *
import datetime as dt
from spread_model.model_management import ModelManagement 
from pandas.tseries.offsets import MonthEnd, MonthBegin

ROLLING_DATA = 12

class FundNAV():
    def __init__(self):
        self.date_columns = ['As Of Date', 'Begin Date']
        self.fund_df = self.get_data_from_file()
        self.fund_ratios_df = None
        self.nav_data = None
        self.class_benchmark_df = None

    def get_data_from_file(self):
        dir_path = fad_utils.get_data_sample_dir_path()
        fund_df = pd.read_csv(dir_path + file_cst.FUND_NAV_FILE, index_col=None, parse_dates=self.date_columns, infer_datetime_format=True)
        return fund_df

    def get_beta(self, fund_nav_data_df, benchmark_data):
        benchmark_list =  [tuple(x) for x in benchmark_data.values]
        fund_nav_list =  [tuple(x) for x in fund_nav_data_df.values]

        window = ROLLING_DATA if len(benchmark_list) > 12 else len(benchmark_list) - 1
        fund_beta = get_beta(fund_nav_list, benchmark_list, window)
        return fund_beta

    def get_beta_by_fund_row(self, report_acc_ben, fund_row, sp500_df, list_date):
        report_acc_num = fund_row['Reporting Account Number']
        source_acc_num = fund_row['Source Account Number']
        source_acc_name = fund_row['Source Account Name']

        benchmark_return_df = ModelManagement().benchmark_model.get_bechmark_return_in_range_date(source_acc_num, source_acc_name, list_date)

        fund_beta = ''
        if benchmark_return_df is None or benchmark_return_df.empty:
            fund_beta = 'Not have CRBM'
        else:
            
            benchmark_return_df['nav'] = benchmark_return_df['CRBM'].cumprod()
            report_acc_ben['source_nav'] = benchmark_return_df['nav']
            if report_acc_ben[report_acc_num].isnull().any() :
                report_acc_ben[report_acc_num] = report_acc_ben['source_nav']
            else:
                report_acc_ben[report_acc_num] = report_acc_ben[report_acc_num] + report_acc_ben['source_nav']

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

    def get_class_beta(self, report_acc_ben, row, sp500_df, list_date):
        report_acc_number = row['Reporting Account Number']
        class_beta = ''
        if report_acc_ben[report_acc_number].isnull().any() :
            class_beta = 'Can not calculate'
        else:
            class_nav_data_df = pd.DataFrame({
                'date': list_date.to_numpy(),
                'nav': report_acc_ben[report_acc_number].to_numpy()
            })

            sp_benchmark_custom_df = pd.DataFrame({
                'date': list_date.to_numpy(),
                'nav': sp500_df['SP500'].to_numpy()
            })
            
            class_beta = self.get_beta(class_nav_data_df, sp_benchmark_custom_df)
        return class_beta

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

        start_sp500_date = sp500_df.iloc[0]['Date']
        benchmark_list_date = ModelManagement().benchmark_model.get_date_list_in_benchmark(start_sp500_date)
        sp5000_index_by_date_df = get_sp500_data_by_date(benchmark_list_date)

        columns_filters = ['Reporting Account Number', 'Reporting Account Name', 'Source Account Number', 
                            'Source Account Name', 'Begin Date']

        fund_filter_fd = self.fund_df[columns_filters]
        self.fund_ratios_df = fund_filter_fd.groupby(['Reporting Account Number', 'Source Account Number']).first().reset_index()
        report_acc = fund_filter_fd[['Reporting Account Number']].groupby(['Reporting Account Number']).first()
        report_acc_benchmark = report_acc.T

        self.fund_ratios_df['Beta'] = self.fund_ratios_df.apply(lambda row: self.get_beta_by_fund_row(report_acc_benchmark, row, sp5000_index_by_date_df, benchmark_list_date), axis=1)

        report_acc = report_acc.reset_index()
        report_acc['Class Beta'] = report_acc.apply(lambda row: self.get_class_beta(report_acc_benchmark, row, sp5000_index_by_date_df, benchmark_list_date), axis=1)
        
        self.class_benchmark_df = fund_filter_fd[['Reporting Account Number','Reporting Account Name']].groupby(['Reporting Account Number']).first()
        self.class_benchmark_df = self.class_benchmark_df.join(report_acc.set_index('Reporting Account Number')).reset_index()
        
    def export_ratios(self):
        dir_path = fad_utils.get_data_sample_dir_path()
        self.fund_ratios_df.to_csv(dir_path + file_cst.FUND_RATIOS_FILE, index=False)

    def export_nav_cal(self, nav_df = None):
        export_nav = nav_df
        if nav_df is None:
            export_nav = self.nav_data

        dir_path = fad_utils.get_data_sample_dir_path()
        export_nav.to_csv(dir_path + file_cst.FUND_NAV_CAL_FILE, index=False)

    def get_begin_nav_by_group(self, fund_fd):
        fund_grouped_by_report = fund_fd.groupby(['Reporting Account Number', 'As Of Date']).sum() \
                                                    .groupby(level=0).cumsum().reset_index()
        return fund_grouped_by_report

    def get_end_nav(self, fund_row):

        transaction_df = ModelManagement().transaction_model.get_transaction(fund_row['Reporting Account Number'], fund_row['Source Account Number'], fund_row['As Of Date'], fund_row['End Date'])
        transaction_df['date'] = transaction_df['Effective Date']
        transaction_df['value'] = transaction_df['Base Txn Amount']
        return get_end_nav(fund_row['Total Market Value'], fund_row['BM'], transaction_df, fund_row['As Of Date'], fund_row['End Date'])

    def calculate_nav_data(self):
        columns_filters = ['Reporting Account Number', 'Reporting Account Name', 'Source Account Number', 
                            'Source Account Name', 'Begin Date', 'As Of Date', 'Total Market Value']

        self.nav_data = self.fund_df[columns_filters]
        self.nav_data = self.nav_data[self.nav_data.groupby(['Reporting Account Number', 'Source Account Number'])['As Of Date'].transform('max') == self.nav_data['As Of Date']]

        self.nav_data['End Date'] = pd.to_datetime(self.nav_data['As Of Date']) + MonthEnd(1)
        self.nav_data['BM'] = self.nav_data.apply(lambda row: ModelManagement().benchmark_model.get_bechmark_return_by_acc_date(row['Source Account Number'], row['Source Account Name'], row['End Date']), axis=1)
        self.nav_data['End NAV'] = self.nav_data.apply(lambda row: self.get_end_nav(row), axis=1)
        self.nav_data['ROR'] = (self.nav_data['End NAV'] - self.nav_data['Total Market Value'])/self.nav_data['Total Market Value']
    
    def get_class_beta_report(self):
        return self.class_benchmark_df
    
    def get_ratios_fund_report(self):
        return self.fund_ratios_df

    def export_class_beta_report(self):
        dir_path = fad_utils.get_data_sample_dir_path()
        self.class_benchmark_df.to_csv(dir_path + file_cst.CLASS_RATIOS_FILE, index=False)