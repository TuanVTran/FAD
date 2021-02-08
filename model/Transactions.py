import pandas as pd
import datetime

class Transactions:
    def __init__(self, data):
        self.data = data
        self.data.sort_values(by=['Date', 'Fund ID'])

    def parseData(self):
        _columns = self.data.columns
        
    def get_fund_transaction(self, fund_id, begin_date, end_date):
        return self.data[(self.data['Fund ID'] == fund_id) & (self.data['Date'] <= end_date) & (self.data['Date'] >= begin_date)]

    def cash_flow_by_date(self, fund_id, begin_date, end_date):
        fund_trans = self.get_fund_transaction(fund_id, begin_date, end_date)
        cash_flow_list = pd.Series([])
        for i, row in fund_trans.iterrows():
            #date_flow = row['Date']
            date_time_obj = row['Date'].strftime('%Y-%m-%d %H:%M:%S') 
            trans_value = row['Trans Value']
            if row['Trans Type'] == 'Sell':
                trans_value *= -1
            
            if date_time_obj in cash_flow_list:
                cash_flow_list[date_time_obj] += trans_value
            else:
                cash_flow_list[date_time_obj] = trans_value

        return cash_flow_list