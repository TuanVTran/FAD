import pandas as pd
import numpy as np

from ..utils import utilities as utils
from .model_management import ModelManagement
from .caculator import Calculator
from ..utils import model_utilities as model_utils
import constant.configuration as constant

class FundRORSummary:
    def __init__(self):
        self.columns = ['Begin Date', 'Fund ID', 'Begin NAV', 'End NAV', 'End Date', 'ROR', 'Classification']
        self.ror_data = pd.DataFrame(data=None, columns=self.columns)
        self.classifications = {}
    
    def add_fund_summary(self, fund_id, fund_nav, begin_date, classification, cash_flow_list, end_date, end_NAV, ror):
        
        # build cash_flow list to export data
        exported_cash_flow = model_utils.build_cash_flow_to_export(cash_flow_list)
        fund_series = pd.Series(np.array([begin_date, fund_id, fund_nav, end_NAV, end_date, ror, classification]), index=self.columns)
        fund_series = fund_series.append(exported_cash_flow)
        self.ror_data = self.ror_data.append(fund_series, ignore_index=True)

    def export_data(self, filePath = None):
        if filePath == None:
            filePath = utils.get_data_dir_path() + constant.ROR_FILE

        self.ror_data.round(2)
        utils.exportToCSV(self.ror_data, filePath)

    def calculate_ror_summary_by_fund(self, fund_id, fund_nav, classification, begin_date, end_date, price_end_date):
        cash_flow_list = ModelManagement().transaction_model.cash_flow_by_date(fund_id, begin_date, end_date)
        fund_benchmark = ModelManagement().benchmark_model.get_fund_benchmark(fund_id)
        price_begin_date = ModelManagement().price_model.get_prices(begin_date)

        cash_flow_weight = Calculator().calculate_weight_cash_flow(cash_flow_list)
        return_of_benchmark = Calculator().calculate_return_of_benchmark(fund_benchmark, price_begin_date, price_end_date)

        end_NAV = Calculator().calculate_end_NAV(fund_nav, cash_flow_weight, return_of_benchmark)
        rate_of_return = Calculator().calculate_rate_of_return(fund_nav, end_NAV)

        self.add_fund_summary(fund_id, fund_nav, begin_date, classification, cash_flow_list, end_date, end_NAV, rate_of_return)
    
    def calculate_ror_summary(self, end_date):
        
        price_end_date = ModelManagement().price_model.get_prices(end_date)
        summary_model = ModelManagement().summary_model
        funds = summary_model.get_funds()
        for i,r in funds.iterrows():
            fund_id = summary_model.get_fund_id_by_row(r)
            begin_date = summary_model.get_date_by_row(r)
            fund_nav = summary_model.get_nav_by_row(r)
            class_name = summary_model.get_class_name_by_row(r)
            class_id = summary_model.get_class_id_by_row(r)

            self.calculate_ror_summary_by_fund(fund_id, fund_nav, class_name, begin_date, end_date, price_end_date)
            if class_id in self.classifications:
                self.classifications[class_id]['begin_nav']  += fund_nav
                self.classifications[class_id]['funds'].append(fund_id)
            else:
                self.classifications[class_id] = {}
                self.classifications[class_id]['name'] = class_name
                self.classifications[class_id]['begin_date'] = begin_date
                self.classifications[class_id]['begin_nav'] = fund_nav
                self.classifications[class_id]['funds'] = [fund_id]
        
        return self.classifications