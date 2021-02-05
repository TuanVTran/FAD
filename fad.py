import pandas as pd
import datetime as dt
import time
import numpy as np
import sys

from model import Caculator as cl
from model import FundSummary as fund
from model import FundBenchmark as fundBen
from model import Transactions as trans
from model import Prices as prices
from model import FundRORSummary as fund_ror
from service import data_service
import utils.Utilities as utils

FILEDIR = r"E:\\SourceCode\\Python\\FAD\\"
FILENAME = "ManagerLevel.xlsx"
FILE_CSV = "ManagerLevel.csv"

DATADIR = r"E:\\SourceCode\\Python\\FAD\\data\\"
FUND_BENMARK = "FundBenchMark.csv"
FUND_SUMMARY = "FundSummary.csv"
PRICE = "Price.csv"
TRANSACTION = "Transaction.csv"

def calculate_weight_cash_flow(fund_trans):
    weight_cash_flow = 0
    cash_flow_list = {}
    for i,row in fund_trans.iterrows():
        trans_value = row['Trans Value']
        trans_output = str(trans_value)
        if row['Trans Type'] == 'Buy':
            weight_cash_flow += trans_value
            trans_output = '+' + trans_output
        elif row['Trans Type'] == 'Sell':
            weight_cash_flow -= trans_value
            trans_output = '-' + trans_output
        cash_flow_list['Day ' + str(row['Date']) + 'Flow'] = trans_output
    
    return {
            'weight_cash_flow': weight_cash_flow, 
            'cash_flow_list': cash_flow_list
        }

def calculate_return_of_benchmark(fund_benchmark, price_begin_date, price_end_date):
    return_of_benchmark = 0
    for i,row in fund_benchmark.iterrows():
        begin_price = price_begin_date[price_begin_date['Security ID'] == row['Security ID']].iloc[0]['Price']
        end_price = price_end_date[price_end_date['Security ID'] == row['Security ID']].iloc[0]['Price']
        return_of_benchmark += int(row['Weight']) * (int(end_price) - int(begin_price))/int(begin_price)
    
    return return_of_benchmark



def exportRORSummary(data_service, fund_id, end_date_str):
    end_date = utils.to_date(end_date_str)

    fund_infor = data_service['fundSumary'].get_fund(fund_id)
    fund_trans = data_service['transaction'].get_fund_transaction(fund_id, fund_infor.Date, np.datetime64(end_date))
    fund_benchmark = data_service['benchmark'].get_fund_benchmark(fund_id)
    price_begin_date = data_service['price'].get_prices(fund_infor.Date)
    price_end_date = data_service['price'].get_prices(np.datetime64(end_date))

    cash_flow = calculate_weight_cash_flow(fund_trans)
    return_of_benchmark = calculate_return_of_benchmark(fund_benchmark, price_begin_date, price_end_date)

    end_NAV = (fund_infor['NAV'] + cash_flow['weight_cash_flow']) * (1 + return_of_benchmark)
    rate_of_return = (end_NAV - fund_infor['NAV'])/fund_infor['NAV']

    end_NAV = round(end_NAV, 2)
    rate_of_return = round(rate_of_return, 2)

    for_summary = fund_ror.FundRORSummary()
    for_summary.add_fund_summary(fund_infor, cash_flow['cash_flow_list'], end_date, end_NAV, rate_of_return)
    for_summary.export_data()

def parse_data():

    benchmark_data = utils.parseCSV(DATADIR, FUND_BENMARK)
    fundsummary_data = utils.parseCSV(DATADIR, FUND_SUMMARY)
    price_data = utils.parseCSV(DATADIR, PRICE)
    transaction_data = utils.parseCSV(DATADIR, TRANSACTION)

    fundSumary = fund.FundSummary(fundsummary_data)
    transaction = trans.Transactions(transaction_data)
    benchmark = fundBen.FundBenchmark(benchmark_data)
    price = prices.Prices(price_data)

    return {'fundSumary': fundSumary, 'transaction': transaction, 'benchmark': benchmark, 'price': price}

def main():

    service = parse_data()
    fund_ids = service['fundSumary'].get_fund_ids()
    print('List of funds: ', fund_ids)
    fund_id = input ("Please select fund to calulate:")
    end_date = input ("Enter the end date of Fund:")  
    exportRORSummary(service, fund_id, end_date)

if __name__ == '__main__':
    main()