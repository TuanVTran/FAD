import pandas as pd
from .model_management import ModelManagement

class _Caculator:
    _instance = None
    def __init__(self):
       self.formulars = {}

    def calculate_weight_cash_flow(self, cash_flow_list):
        weight_cash_flow = 0
        for value in cash_flow_list:
            weight_cash_flow += value

        return weight_cash_flow

    def calculate_return_of_benchmark(self, fund_benchmark, price_begin_date, price_end_date):
        return_of_benchmark = 0
        for i,row in fund_benchmark.iterrows():
            security_id = ModelManagement().benchmark_model.get_security_by_row(row)
            security_weight = ModelManagement().benchmark_model.get_weight_by_row(row)
            
            begin_price = ModelManagement().price_model.get_price_by_security(price_begin_date, security_id)
            end_price = ModelManagement().price_model.get_price_by_security(price_end_date, security_id)
            return_of_benchmark += security_weight * (end_price - begin_price)/begin_price
        
        return return_of_benchmark

    def calculate_end_NAV(self, begin_NAV, weight_cash_flow, return_of_benchmark):
        end_NAV = (begin_NAV + weight_cash_flow) * (1 + return_of_benchmark)
        return end_NAV
    
    def calculate_end_NAV_by_flow(self, begin_NAV, weight_cash_flow, return_of_benchmark, begin_date, end_date):
        between_day = (end_date - begin_date).days
        flow_return = 0
        for i in range(1,between_day+1):
            flow_return = weight_cash_flow * (1 + return_of_benchmark * (between_day - i)/between_day)
        end_NAV = begin_NAV * (1 + return_of_benchmark) + flow_return
        return end_NAV

    def calculate_rate_of_return(self, begin_NAV, end_NAV):
        return (end_NAV - begin_NAV)/begin_NAV
        
    def calculate_policy_weight_cash_flow(self, fund_benchmark, price_begin_date, price_end_date):
        pass

def Calculator():
    if _Caculator._instance is None:
        _Caculator._instance = _Caculator()
    return _Caculator._instance
