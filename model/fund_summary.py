
import pandas as pd

FUND_ID_COL = 'Fund ID'
NAV_COL = 'NAV'
CLASS_NAME_COL = 'Classification'
CLASS_ID_COL = 'Class ID'
DATE_COL = 'Date'

class FundSummary:
    def __init__(self, data):
        self.data = data
        
    def get_fund(self, fund_id):
        fund_summary = self.data.loc[self.data[FUND_ID_COL] == fund_id]
        return fund_summary.iloc[0]
        
    def get_fund_ids(self):
        return self.data[FUND_ID_COL].values

    def get_funds(self):
        return self.data

    def get_fund_id_by_row(self, row):
        return row[FUND_ID_COL]
    
    def get_nav_by_row(self, row):
        return row[NAV_COL]
    
    def get_class_name_by_row(self, row):
        return row[CLASS_NAME_COL]
    
    def get_class_id_by_row(self, row):
        return row[CLASS_ID_COL]
    
    def get_date_by_row(self, row):
        return row[DATE_COL]