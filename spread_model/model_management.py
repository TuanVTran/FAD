

class _ModelManagement:
    _instance = None
    def __init__(self):
        self.fund_nav_model = None
        self.transaction_model = None
        self.benchmark_model = None
        pass

    def add_fund_nav_model(self, fund_nav_model):
        self.fund_nav_model = fund_nav_model

    def add_transaction_model(self, trans_model):
        self.transaction_model = trans_model
    
    def add_benchmark_model(self, benchmark_model):
        self.benchmark_model = benchmark_model

def ModelManagement():
    if _ModelManagement._instance is None:
        _ModelManagement._instance = _ModelManagement()
    return _ModelManagement._instance