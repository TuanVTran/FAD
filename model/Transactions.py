import pandas as pd

class Transactions:
    def __init__(self, data):
        self.data = data

    def parseData(self):
        _columns = self.data.columns
        
    def get_fund_transaction(self, fund_id, begin_date, end_date):
        return self.data[(self.data['Fund ID'] == fund_id) & (self.data['Date'] <= end_date) & (self.data['Date'] >= begin_date)]