import pandas as pd
import numpy as np

from utils import utilities as utils
from .model_management import ModelManagement
from .caculator import Calculator
from utils import model_utilities as model_utils
import constant.configuration as constant

class ClassificationSummary:

    def __init__(self, classification):
        self.begin_columns = ['Begin Date', 'Class ID', 'Classification', 'Begin NAV']
        self.end_columns = ['End NAV', 'End Date', 'ROR']
        self.classification_data = pd.DataFrame(data=None)
        self.classifications = classification
        
    def calculate_classification_cash_flow(self, funds, begin_date, end_date):
        cash_flow_list = pd.Series([])

        for fund_id in funds:
            cash_flow_list_by_fund = ModelManagement().transaction_model.cash_flow_by_date(fund_id, begin_date, end_date)
            cash_flow_list = cash_flow_list.add(cash_flow_list_by_fund, fill_value=0)

        return cash_flow_list.astype('int64')

    def calculate_classification_summary(self, end_date):
        price_end_date = ModelManagement().price_model.get_prices(end_date)

        for class_id in self.classifications:
            classfication = self.classifications[class_id]
            begin_date = classfication['begin_date']
            begin_nav = classfication['begin_nav']
            funds = classfication['funds']
            class_name = classfication['name']

            policy_benchmark = ModelManagement().policy_benchmark_model.get_policy_benchmark(class_id)
            price_begin_date = ModelManagement().price_model.get_prices(begin_date)

            policy_of_benchmark = Calculator().calculate_return_of_benchmark(policy_benchmark, price_begin_date, price_end_date)
            cash_flow = self.calculate_classification_cash_flow(funds, begin_date, end_date)

            cash_flow_weight = Calculator().calculate_weight_cash_flow(cash_flow)
            end_nav = Calculator().calculate_end_NAV(begin_nav, cash_flow_weight, policy_of_benchmark)
            rate_of_return = Calculator().calculate_rate_of_return(begin_nav, end_nav)

            begin_fund_series = pd.Series(np.array([begin_date, class_id, class_name, begin_nav]), index=self.begin_columns)
            end_fund_series = pd.Series(np.array([end_nav, end_date, rate_of_return]), index=self.end_columns)

            exported_cash_flow = model_utils.build_cash_flow_to_export(cash_flow)
            fund_series = begin_fund_series.append(exported_cash_flow)
            fund_series = fund_series.append(end_fund_series)

            self.classification_data = self.classification_data.append(fund_series, ignore_index=True)
            
        self.classification_data


    def export_data(self, filePath = None):
        if filePath == None:
            filePath = utils.get_data_dir_path() + constant.CLASS_SUMMARY_FILE

        self.classification_data.round(2)
        utils.exportToCSV(self.classification_data, filePath)

    def get_classification(self, class_id):
        self.classifications[class_id] = self.classifications[class_id] | {}
        return self.classifications[class_id]
