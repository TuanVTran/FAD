import pandas as pd

class Prices:
    def __init__(self, data):
        self.data = data

    def get_prices(self, date):
        return self.data[self.data['Date'] == date][['Security ID', 'Price']]