
from model.Parser import Parser
from utils import Utilities as utils

DATADIR = utils.get_data_dir_path()
POLICY_BENMARK = "PolicyBenchMark.csv"
FUND_BENMARK = "FundBenchMark.csv"
FUND_SUMMARY = "FundSummary.csv"
PRICE = "Price.csv"
TRANSACTION = "Transaction.csv"
ROR_FILE = "FundRORSummary.csv"
CLASS_SUMMARY_FILE = "ClassificationSummary.csv"


class CSVParser(Parser):

    def __init__(self):
        pass

    def parse_benchmark_data(self):
        return utils.parseCSV(DATADIR, FUND_BENMARK)
    
    def parse_summary_data(self):
        return utils.parseCSV(DATADIR, FUND_SUMMARY)

    def parse_price_data(self):
        return utils.parseCSV(DATADIR, PRICE)

    def parse_transaction_data(self):
        return utils.parseCSV(DATADIR, TRANSACTION) 
    
    def parse_policy_benchmark_data(self):
        return utils.parseCSV(DATADIR, POLICY_BENMARK)