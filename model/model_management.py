from .fund_summary import FundSummary
from .fund_benchmark import FundBenchmark
from .transactions import Transactions
from .prices import Prices
from .policy_benchmark import PolicyBenchmark
 
class _ModelManagement:
    _instance = None
    def __init__(self):
        pass

    def addFundSummaryModel(self, fundsummary_data):
        fundSumary = FundSummary(fundsummary_data)
        self.summary_model = fundSumary

    def addTransactionModel(self, transaction_data):
        transaction = Transactions(transaction_data)
        self.transaction_model = transaction
    
    def addBenchMarkModel(self, benchmark_data):
        benchmark = FundBenchmark(benchmark_data)
        self.benchmark_model = benchmark
    
    def addPriceModel(self, price_data):
        price = Prices(price_data)
        self.price_model = price
    
    def addPolicyBenchMarkModel(self, policy_benchmark_data):
        policy_benchmark = PolicyBenchmark(policy_benchmark_data)
        self.policy_benchmark_model = policy_benchmark

def ModelManagement():
    if _ModelManagement._instance is None:
        _ModelManagement._instance = _ModelManagement()
    return _ModelManagement._instance