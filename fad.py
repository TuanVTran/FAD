import pandas as pd
import datetime as dt
import time
import numpy as np
import sys

from model.fund_ror_summary import FundRORSummary
from model.classification_summary import ClassificationSummary
from model.model_management import ModelManagement
from model.csv_parser import CSVParser

def exportSummary():
    end_date = dt.date.today()
    np_end_date = np.datetime64(end_date)

    for_summary = FundRORSummary()
    classification = for_summary.calculate_ror_summary(np_end_date)
    for_summary.export_data()

    classification_summary = ClassificationSummary(classification)
    classification_summary.calculate_classification_summary(np_end_date)
    classification_summary.export_data()

def parse_data():

    parser = CSVParser()

    benchmark_data = parser.parse_benchmark_data()
    fundsummary_data = parser.parse_summary_data()
    price_data = parser.parse_price_data()
    transaction_data = parser.parse_transaction_data()
    policy_benchmark_data = parser.parse_policy_benchmark_data()

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