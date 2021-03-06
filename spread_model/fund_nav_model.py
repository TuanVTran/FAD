
import constant.configuration as constant
import utils.utilities as utils
import pandas as pd
from calculator.fad_calculator import *
import datetime as dt
from spread_model.trans_model import Transaction 
from spread_model.benchmark_model import BenchmarkReturn 

ROLLING_DATA = 12

class FundNAV():
    def __init__(self):
        self.date_columns = ['As Of Date', 'Begin Date']
        self.fund_df = self.get_data_from_file()
        self.fund_ratios_df = pd.DataFrame(columns=['Reporting Account Number', 'Reporting Account Name', 'Source Account Number', 
                            'Source Account Name', 'Begin Date'])
        self.nav_data = None
        self.benchmark = BenchmarkReturn()

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

    def get_nav_df_data(self):
        if self.nav_data is not None:
            return self.nav_data

        # use the nav data in exsit file
        columns_filters = ['Reporting Account Number', 'Reporting Account Name', 'Source Account Number', 
                            'Source Account Name', 'Begin Date', 'As Of Date', 'Total Market Value']

        fund_filter_fd = self.fund_df[columns_filters].copy()
        fund_filter_fd['End Date'] = fund_filter_fd['As Of Date']
        fund_filter_fd['End NAV'] = fund_filter_fd['Total Market Value']
        return fund_filter_fd

    def calculate_fund_ratios(self, benchmark_df):
        
        # get benchmark data in and get the working day of sp500 index
        def get_benchmark_data_by_date(source_date_data):
            working_date_list = []
            for date in source_date_data:
                working_date = date
                if date.day_of_week >= 5:
                    working_date = date - dt.timedelta(date.day_of_week - 4)

                while benchmark_df[benchmark_df['Date'] == working_date].empty :
                    working_date = working_date - dt.timedelta(1)

                working_date_list.append(working_date)
            return benchmark_df[benchmark_df['Date'].isin(working_date_list)]

        nav_fd = self.get_nav_df_data()
        nav_grouped_fund = nav_fd.groupby(['Reporting Account Number', 'Source Account Number'])

        for gr_name, group in nav_grouped_fund:
            source_acc_num_group = group

            export_fund_df = source_acc_num_group[['Reporting Account Number', 'Reporting Account Name', 'Source Account Number', 
                            'Source Account Name', 'Begin Date']]

            acc_row = export_fund_df.iloc[-1]

            source_acc_num = gr_name[1]
            source_acc_name = acc_row['Source Account Name']

            start_benmarck_date = benchmark_df.iloc[0]['Date']
            benchmark_return_df = self.benchmark.get_bechmark_return_by_acc(source_acc_num, source_acc_name, start_benmarck_date)

            fund_beta = ''
            if benchmark_return_df is None or benchmark_return_df.empty:
                fund_beta = 'Not have CRBM'
            else:
                source_date_data = benchmark_return_df['Date']
                sp_benchmark_df = get_benchmark_data_by_date(source_date_data)

                benchmark_return_df['nav'] = benchmark_return_df['CRBM'].cumprod()
                fund_nav_data_df = pd.DataFrame({
                    'date': source_date_data.to_numpy(),
                    'nav': benchmark_return_df['nav'].to_numpy()
                })

                sp_benchmark_custom_df = pd.DataFrame({
                    'date': source_date_data.to_numpy(),
                    'nav': sp_benchmark_df['SP500'].to_numpy()
                })
                
                fund_beta = self.get_beta(fund_nav_data_df, sp_benchmark_custom_df)

            # add into radio_df to export
            acc_row['Beta'] = fund_beta
            self.fund_ratios_df = self.fund_ratios_df.append(acc_row)

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

    def get_end_nav(self, begin_nav, benchmark_return, transaction_df, from_date, to_date):
        
        # get comosite dataframe to calculate benchmark
        
        trans_df = transaction_df.copy()
        trans_df['date'] = transaction_df['Effective Date']
        trans_df['value'] = transaction_df['Base Txn Amount']
        return get_end_nav(begin_nav, benchmark_return, trans_df, from_date, to_date)

    def calculate_nav_data(self):
        columns_filters = ['Reporting Account Number', 'Reporting Account Name', 'Source Account Number', 
                            'Source Account Name', 'Begin Date', 'As Of Date', 'Total Market Value']

        fund_filter_fd = self.fund_df[columns_filters]
        security_grouped_fund = fund_filter_fd.groupby(['Reporting Account Number', 'Source Account Number'])

        nav_cal_df = pd.DataFrame(columns=['Reporting Account Number', 'Reporting Account Name', 'Source Account Number', 
                            'Source Account Name', 'Begin Date','As Of Date', 'Total Market Value'])

        trans = Transaction()
        nav_in_group_by_date = self.get_begin_nav_by_group(fund_filter_fd)

        for name, group in security_grouped_fund:
            source_acc_num = name
            source_acc_num_group = group

            export_fund_df = source_acc_num_group[['Reporting Account Number', 'Reporting Account Name', 'Source Account Number', 
                            'Source Account Name', 'Begin Date', 'As Of Date', 'Total Market Value']]

            acc_row = export_fund_df.iloc[-1]
            report_number = acc_row['Reporting Account Number']
            source_number = acc_row['Source Account Number']
            source_name = acc_row['Source Account Name']
            current_nav = acc_row['Total Market Value']
            as_date = acc_row['As Of Date']

            start_next_month = utils.get_start_next_month(as_date)
            end_next_month = utils.get_end_month(start_next_month)

            transaction_df = trans.get_transaction(report_number, source_number, as_date, end_next_month)
            total_txn_amount = trans.get_total_base_txn_amount(transaction_df)

            benchmark_return = self.benchmark.get_bechmark_return_by_acc_date(source_number, source_name, end_next_month)
            
            acc_row['End Date'] = end_next_month
            acc_row['End NAV'] = self.get_end_nav(current_nav, benchmark_return, transaction_df, as_date, end_next_month)
            acc_row['ROR'] = (acc_row['End NAV'] - current_nav)/current_nav
            nav_cal_df = nav_cal_df.append(acc_row)

        self.nav_data = nav_cal_df

