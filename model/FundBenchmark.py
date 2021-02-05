import pandas as pd

class FundBenchmark:
    def __init__(self, data):
        self.data = data

    def parseData(self):
        _columns = self.data.columns
    
    def get_fund_benchmark(self, fund_id):
        return self.data[self.data['Fund ID'] == fund_id]