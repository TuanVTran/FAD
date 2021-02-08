import pandas as pd

class FundBenchmark:
    def __init__(self, data):
        self.data = data

    def parseData(self):
        _columns = self.data.columns
    
    def get_fund_benchmark(self, fund_id):
        return self.data[self.data['Fund ID'] == fund_id]

    def calculate_return_of_benchmark(self, fund_benchmark, price_begin_date, price_end_date):
        return_of_benchmark = 0
        for i,row in fund_benchmark.iterrows():
            begin_price = price_begin_date[price_begin_date['Security ID'] == row['Security ID']].iloc[0]['Price']
            end_price = price_end_date[price_end_date['Security ID'] == row['Security ID']].iloc[0]['Price']
            return_of_benchmark += row['Weight'] * (end_price - begin_price)/begin_price
        
        return return_of_benchmark
    
    def get_security_by_row(self, row):
        return row['Security ID']

    def get_weight_by_row(self, row):
        return row['Weight']