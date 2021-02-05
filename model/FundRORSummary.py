import pandas as pd
import numpy as np

from utils import Utilities as utils
from model.ModelManagement import ModelManagement
from model.Caculator import Calculator

class FundRORSummary:
    def __init__(self):
        self.columns = ['Begin Date', 'Fund ID', 'Begin NAV', 'End NAV', 'End Date', 'ROR', 'Classification']
        self.ror_data = pd.DataFrame(data=None, columns=self.columns)
        
    def add_fund_summary(self, fund_id, fund_nav, begin_date, classification, cash_flow_list, end_date, end_NAV, ror):
        fund_series = pd.Series(np.array([begin_date, fund_id, fund_nav, end_NAV, end_date, ror, classification]), index=self.columns)
        self.ror_data = self.ror_data.append(fund_series, ignore_index=True)

    def export_data(self, filePath):
        self.ror_data.round(2)
        utils.exportToCSV(self.ror_data, filePath)

    def calculate_ror_summary(self, fund_id, fund_nav, classification, begin_date, end_date, price_end_date):
        fund_trans = ModelManagement().transaction_model.get_fund_transaction(fund_id, begin_date, end_date)
        fund_benchmark = ModelManagement().benchmark_model.get_fund_benchmark(fund_id)
        price_begin_date = ModelManagement().price_model.get_prices(begin_date)

        cash_flow = Calculator().calculate_weight_cash_flow(fund_trans)
        return_of_benchmark = Calculator().calculate_return_of_benchmark(fund_benchmark, price_begin_date, price_end_date)

        end_NAV = Calculator().calculate_end_NAV(fund_nav, cash_flow['weight_cash_flow'], return_of_benchmark)
        rate_of_return = Calculator().calculate_rate_of_return(fund_nav, end_NAV)

        self.add_fund_summary(fund_id, fund_nav, begin_date, classification, cash_flow['cash_flow_list'], end_date, end_NAV, rate_of_return)