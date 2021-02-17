import pandas as pd
import numpy as np

FUND_ID_COL = 'Fund ID'
SECURITY_ID_COL = 'Security ID'
PRICE_COL = 'Price'
DATE_COL = 'Date'


class Prices:
    def __init__(self, data):
        self.data = data
        self.data.sort_values(by=[DATE_COL])

    def get_prices(self, date):
        closest_date = self.data.iloc[:-1][DATE_COL].values[0]
        return self.data[(self.data[DATE_COL] == date) | (self.data[DATE_COL] == closest_date)][[SECURITY_ID_COL, PRICE_COL]]

    def get_price_by_security(self, date_prices, sec_id):
        return date_prices[date_prices[SECURITY_ID_COL] == sec_id].iloc[0][PRICE_COL]