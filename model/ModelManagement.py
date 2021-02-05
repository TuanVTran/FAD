
from model import FundSummary as fund
from model import FundBenchmark as fundBen
from model import Transactions as trans
from model import Prices as prices
from model import PolicyBenchmark as pb

class _ModelManagement:
    _instance = None
    def __init__(self):
        pass

    def addFundSummaryModel(self, fundsummary_data):
        fundSumary = fund.FundSummary(fundsummary_data)
        self.summary_model = fundSumary

    def addTransactionModel(self, transaction_data):
        transaction = trans.Transactions(transaction_data)
        self.transaction_model = transaction
    
    def addBenchMarkModel(self, benchmark_data):
        benchmark = fundBen.FundBenchmark(benchmark_data)
        self.benchmark_model = benchmark
    
    def addPriceModel(self, price_data):
        price = prices.Prices(price_data)
        self.price_model = price
    
    def addPolicyBenchMarkModel(self, policy_benchmark_data):
        policy_benchmark = pb.PolicyBenchmark(policy_benchmark_data)
        self.policy_benchmark_model = policy_benchmark

def ModelManagement():
    if _ModelManagement._instance is None:
        _ModelManagement._instance = _ModelManagement()
    return _ModelManagement._instance