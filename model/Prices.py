import pandas as pd
import numpy as np

class Prices:
    def __init__(self, data):
        self.data = data
        self.data.sort_values(by=['Date'])

    def get_prices(self, date):
        # return self.data[self.data['Date'] == date][['Security ID', 'Price']]
        closest_date = self.data.iloc[:-1]['Date'].values[0]
        return self.data[(self.data['Date'] == date) | (self.data['Date'] == closest_date)][['Security ID', 'Price']]

    def get_price_by_security(self, date_prices, sec_id):
        return date_prices[date_prices['Security ID'] == sec_id].iloc[0]['Price']