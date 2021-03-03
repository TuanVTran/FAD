import pandas as pd

FUND_ID_COL = 'Fund ID'
SECURITY_ID_COL = 'Security ID'
PRICE_COL = 'Price'
WEIGHT_COL = 'Weight'

class FundBenchmark:
    def __init__(self, data):
        self.data = data

    def parseData(self):
        _columns = self.data.columns
    
    def get_fund_benchmark(self, fund_id):
        return self.data[self.data[FUND_ID_COL] == fund_id]

    def calculate_return_of_benchmark(self, fund_benchmark, price_begin_date, price_end_date):
        return_of_benchmark = 0
        for i,row in fund_benchmark.iterrows():
            begin_price = price_begin_date[price_begin_date[SECURITY_ID_COL] == row[SECURITY_ID_COL]].iloc[0][PRICE_COL]
            end_price = price_end_date[price_end_date[SECURITY_ID_COL] == row[SECURITY_ID_COL]].iloc[0][PRICE_COL]
            return_of_benchmark += row[WEIGHT_COL] * (end_price - begin_price)/begin_price
        
        return return_of_benchmark
    
    def get_security_by_row(self, row):
        return row[SECURITY_ID_COL]

    def get_weight_by_row(self, row):
        return row[WEIGHT_COL]