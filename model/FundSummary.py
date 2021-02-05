
import pandas as pd

class FundSummary:
    def __init__(self, data):
        self.data = data
        
    def get_fund(self, fund_id):
        fund_summary = self.data.loc[self.data['Fund ID'] == fund_id]
        return fund_summary.iloc[0]
        
    def get_fund_ids(self):
        return self.data['Fund ID'].values

    def get_funds(self):
        return self.data