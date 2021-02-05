import pandas as pd
import numpy as np

from utils import Utilities as utils
from model.ModelManagement import ModelManagement
from model.Caculator import Calculator

class ClassificationSummary:

    def __init__(self):
        self.columns = ['Begin Date', 'Class ID', 'Classification', 'Begin NAV', 'End NAV', 'End Date', 'ROR']
        self.classification_data = pd.DataFrame(data=None, columns=self.columns)
        self.classifications = {}
        
    def add_classification_summary(self, begin_date, class_id, classification, cash_flow_list, begin_nav, end_date, end_NAV, ror):
        fund_series = pd.Series(np.array([begin_date, class_id, classification, begin_nav, end_NAV, end_date, ror]), index=self.columns)
        self.classification_data = self.classification_data.append(fund_series, ignore_index=True)

    def calculate_classification_cash_flow(self, funds, begin_date, end_date):
        cash_flow_list = {}
        weight_cash_flow = 0
        
        for fund_id in funds:
            fund_trans = ModelManagement().transaction_model.get_fund_transaction(fund_id, begin_date, end_date)
            cash_flow = Calculator().calculate_weight_cash_flow(fund_trans)
            weight_cash_flow += cash_flow['weight_cash_flow']

        return {
                'weight_cash_flow': weight_cash_flow, 
                'cash_flow_list': cash_flow_list
            }

    def calculate_classification_summary(self, end_date):
        price_end_date = ModelManagement().price_model.get_prices(end_date)

        for class_id in self.classifications:
            classfication = self.classifications[class_id]
            begin_date = classfication['begin_date']
            begin_nav = classfication['begin_nav']
            funds = classfication['funds']
            policy_benchmark = ModelManagement().policy_benchmark_model.get_policy_benchmark(class_id)
            price_begin_date = ModelManagement().price_model.get_prices(begin_date)

            policy_of_benchmark = Calculator().calculate_return_of_benchmark(policy_benchmark, price_begin_date, price_end_date)
            cash_flow = self.calculate_classification_cash_flow(funds, begin_date, end_date)

            end_nav = Calculator().calculate_end_NAV(begin_nav, cash_flow['weight_cash_flow'], policy_of_benchmark)
            rate_of_return = Calculator().calculate_rate_of_return(begin_nav, end_nav)

            fund_series = pd.Series(np.array([begin_date, class_id, classfication['name'], begin_nav, end_nav, end_date, rate_of_return]), index=self.columns)
            self.classification_data = self.classification_data.append(fund_series, ignore_index=True)

    def export_data(self, filePath):
        self.classification_data.round(2)
        utils.exportToCSV(self.classification_data, filePath)

    def get_classification(self, class_id):
        self.classifications[class_id] = self.classifications[class_id] | {}
        return self.classifications[class_id]

    def add_classification(self, class_id, classification_name, fund_id, begin_date, begin_nav):
        if class_id in self.classifications:
            self.classifications[class_id]['begin_nav']  += begin_nav
            self.classifications[class_id]['funds'].append(fund_id)
        else:
            self.classifications[class_id] = {}
            self.classifications[class_id]['name'] = classification_name
            self.classifications[class_id]['begin_date'] = begin_date
            self.classifications[class_id]['begin_nav'] = begin_nav
            self.classifications[class_id]['funds'] = [fund_id]
