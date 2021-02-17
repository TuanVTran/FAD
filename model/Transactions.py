import pandas as pd
import datetime

FUND_ID_COL = 'Fund ID'
SECURITY_ID_COL = 'Security ID'
DATE_COL = 'Date'
TRANS_VALUE_COL = 'Trans Value'
TRANS_TYPE_COL = 'Trans Type'

class Transactions:
    def __init__(self, data):
        self.data = data
        self.data.sort_values(by=[DATE_COL, FUND_ID_COL])

    def parseData(self):
        _columns = self.data.columns
        
    def get_fund_transaction(self, fund_id, begin_date, end_date):
        return self.data[(self.data[FUND_ID_COL] == fund_id) & (self.data[DATE_COL] <= end_date) & (self.data[DATE_COL] >= begin_date)]

    def cash_flow_by_date(self, fund_id, begin_date, end_date):
        fund_trans = self.get_fund_transaction(fund_id, begin_date, end_date)
        cash_flow_list = pd.Series([])
        for i, row in fund_trans.iterrows():
            date_time_obj = row[DATE_COL].strftime('%Y-%m-%d %H:%M:%S') 
            trans_value = row[TRANS_VALUE_COL]
            if row[TRANS_TYPE_COL] == 'Sell':
                trans_value *= -1
            
            if date_time_obj in cash_flow_list:
                cash_flow_list[date_time_obj] += trans_value
            else:
                cash_flow_list[date_time_obj] = trans_value

        return cash_flow_list