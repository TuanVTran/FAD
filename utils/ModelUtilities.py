import pandas as pd
import datetime as dt

def build_cash_flow_to_export(cash_flow_list):
        exported_cash_flow = pd.Series([])
        for cash_flow_date_str, value in cash_flow_list.items():
            cash_flow_date = dt.datetime.strptime(cash_flow_date_str, "%Y-%m-%d %H:%M:%S")
            date_flow = cash_flow_date.strftime("%m-%d")
            exported_cash_flow['Day ' + date_flow + ' flow'] = value
        return exported_cash_flow