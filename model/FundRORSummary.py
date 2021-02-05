import pandas as pd
import numpy as np

from utils import Utilities as utils

DATADIR = r"E:\\SourceCode\\Python\\FAD\\data\\"
ROR_FILE = "FundRORSummary.csv"

class FundRORSummary:
    def __init__(self):
        self.columns = ['Begin Date', 'Fund ID', 'Begin NAV', 'End NAV', 'End Date', 'ROR', 'Classification']
        self.ror_data = pd.DataFrame(data=None, columns=self.columns)
        
    def add_fund_summary(self, fund_infor: object, cash_flow_list, end_date, end_NAV, ror):
        fund_series = pd.Series(np.array([fund_infor['Date'], fund_infor['Fund ID'], fund_infor['NAV'], end_NAV, end_date, ror, fund_infor['Classification']]), index=self.columns)
        self.ror_data = self.ror_data.append(fund_series, ignore_index=True)

    def export_data(self):
        utils.exportToCSV(self.ror_data, DATADIR, ROR_FILE)