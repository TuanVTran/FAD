import pandas as pd
import datetime as dt
import time
import numpy as np
import os

def read_excel(xl, sheetname):
    df = pd.read_excel(xl.io, sheet_name=sheetname, index_col=0)
    return df

def read_csv(file):
    df = pd.read_csv(file, index_col=None, parse_dates=['Date'])
    return df

def parseData(dir, fileName):
    xl = pd.ExcelFile(dir + fileName)
    site_names = xl.sheet_names
    dfs = {}
    for site_name in site_names:
        dfs[site_name] = read_excel(xl,site_name)
    return site_names, dfs

def readExcelWithSheets(dir, fileName, sheet_list):
    xl = pd.ExcelFile(dir + fileName)
    site_names = xl.sheet_names
    dfs = {}
    for site_name in site_names:
        if site_name in sheet_list:
            dfs[site_name] = read_excel(xl, site_name)
    return dfs

def exportDataToExcel(path, data, sheet_name):
    return ''
    # with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
    #     data.to_excel(writer, index=False, sheet_name=sheet_name)
    #     workbook = writer.bookworksheet = writer.sheets[sheet_name]
    #     header_fmt = workbook.add_format({'bold': True})
    #     workbook.set_row(0, None, header_fmt)
    #     writer.save()

def parseCSV(dir, fileName, columns_date=['Date']):
    df = pd.read_csv(dir + fileName, index_col=None, parse_dates=columns_date)
    return df

def exportToCSV(data, filePath):
    data.to_csv(filePath, index=False)

def to_date(date_str):
    return dt.datetime.strptime(date_str, "%m/%d/%Y").date()

def get_data_dir_path():
    dir_path = os.getcwd()
    return dir_path + "\\data\\"

def get_data_sample_dir_path():
    dir_path = os.getcwd()
    return dir_path + "\\AccountingDataSample\\"

def get_start_next_month(cur_date):
    return (cur_date.replace(day=1) + dt.timedelta(days=32)).replace(day=1)

def get_end_month(cur_date):
    return get_start_next_month(cur_date) - dt.timedelta(1)

def currency_converter(x):
    x = (x.replace( '[\$,)]','', regex=True )
        .replace( '[(]','-', regex=True )
        .replace( '[,]','', regex=True ).astype(float))
    return x

def format_float_number(x):
    return format(x, '.2f')