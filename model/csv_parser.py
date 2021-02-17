
from model.parser import Parser
from utils import utilities as utils
import constant.configuration as constant

DATADIR = utils.get_data_dir_path()

class CSVParser(Parser):

    def __init__(self):
        pass

    def parse_benchmark_data(self):
        return utils.parseCSV(DATADIR, constant.FUND_BENMARK)
    
    def parse_summary_data(self):
        return utils.parseCSV(DATADIR, constant.FUND_SUMMARY)

    def parse_price_data(self):
        return utils.parseCSV(DATADIR, constant.PRICE)

    def parse_transaction_data(self):
        return utils.parseCSV(DATADIR, constant.TRANSACTION) 
    
    def parse_policy_benchmark_data(self):
        return utils.parseCSV(DATADIR, constant.POLICY_BENMARK)