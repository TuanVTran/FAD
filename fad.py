import pandas as pd
import datetime as dt
import time
import numpy as np
import sys
import os

from model import FundRORSummary as fund_ror
from model import ClassificationSummary as class_ror
from service import data_service
import utils.Utilities as utils
from model.ModelManagement import ModelManagement

dir_path = os.path.dirname(os.path.realpath(__file__))

DATADIR = dir_path + "\\data\\"
POLICY_BENMARK = "PolicyBenchMark.csv"
FUND_BENMARK = "FundBenchMark.csv"
FUND_SUMMARY = "FundSummary.csv"
PRICE = "Price.csv"
TRANSACTION = "Transaction.csv"
ROR_FILE = "FundRORSummary.csv"
CLASS_SUMMARY_FILE = "ClassificationSummary.csv"

def exportSummary():
    end_date = dt.date.today()
    np_end_date = np.datetime64(end_date)
    for_summary = fund_ror.FundRORSummary()
    classification_summary = class_ror.ClassificationSummary()
    price_end_date = ModelManagement().price_model.get_prices(np_end_date)

    funds = ModelManagement().summary_model.get_funds()
    for i,r in funds.iterrows():
        fund_id = r['Fund ID']
        begin_date = r['Date']
        fund_nav = r['NAV']
        classification_name = r['Classification']
        classification_id = r['Class ID']

        for_summary.calculate_ror_summary(fund_id, fund_nav, classification_name, begin_date, np_end_date, price_end_date)
        classification_summary.add_classification(classification_id, classification_name, fund_id, begin_date, fund_nav)

    for_summary.export_data(DATADIR + ROR_FILE)
    classification_summary.calculate_classification_summary(np_end_date)
    classification_summary.export_data(DATADIR + CLASS_SUMMARY_FILE)

def parse_data():

    benchmark_data = utils.parseCSV(DATADIR, FUND_BENMARK)
    fundsummary_data = utils.parseCSV(DATADIR, FUND_SUMMARY)
    price_data = utils.parseCSV(DATADIR, PRICE)
    transaction_data = utils.parseCSV(DATADIR, TRANSACTION)
    policy_benchmark_data = utils.parseCSV(DATADIR, POLICY_BENMARK)

    ModelManagement().addFundSummaryModel(fundsummary_data)
    ModelManagement().addTransactionModel(transaction_data)
    ModelManagement().addBenchMarkModel(benchmark_data)
    ModelManagement().addPriceModel(price_data)
    ModelManagement().addPolicyBenchMarkModel(policy_benchmark_data)

def main():

    parse_data()
    exportSummary()

if __name__ == '__main__':
    main()