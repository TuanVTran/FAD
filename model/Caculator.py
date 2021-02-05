import pandas as pd

class _Caculator:
    _instance = None
    def __init__(self):
       self.formulars = {}

    def calculate_weight_cash_flow(self, fund_trans):
        weight_cash_flow = 0
        cash_flow_list = {}
        for i, row in fund_trans.iterrows():
            date_flow = row['Date'].strftime("%m-%d")
            trans_value = row['Trans Value']
            if row['Trans Type'] == 'Buy':
                weight_cash_flow += trans_value
            elif row['Trans Type'] == 'Sell':
                weight_cash_flow -= trans_value
            
            key = 'Day ' + date_flow + ' Flow'
            if key in cash_flow_list:
                cash_flow_list[key] += trans_value
            else:
                cash_flow_list[key] = 0
        
        return {
                'weight_cash_flow': weight_cash_flow, 
                'cash_flow_list': cash_flow_list
            }

    def calculate_return_of_benchmark(self, fund_benchmark, price_begin_date, price_end_date):
        return_of_benchmark = 0
        for i,row in fund_benchmark.iterrows():
            begin_price = price_begin_date[price_begin_date['Security ID'] == row['Security ID']].iloc[0]['Price']
            end_price = price_end_date[price_end_date['Security ID'] == row['Security ID']].iloc[0]['Price']
            return_of_benchmark += row['Weight'] * (end_price - begin_price)/begin_price
        
        return return_of_benchmark

    def calculate_end_NAV(self, begin_NAV, weight_cash_flow, return_of_benchmark):
        end_NAV = (begin_NAV + weight_cash_flow) * (1 + return_of_benchmark)
        return end_NAV
    
    def calculate_rate_of_return(self, begin_NAV, end_NAV):
        return (end_NAV - begin_NAV)/begin_NAV
        
    def calculate_policy_weight_cash_flow(self, fund_benchmark, price_begin_date, price_end_date):
        pass

def Calculator():
    if _Caculator._instance is None:
        _Caculator._instance = _Caculator()
    return _Caculator._instance
