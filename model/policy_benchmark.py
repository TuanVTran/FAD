import pandas as pd

POLICY_ID_COL = 'Policy ID'
class PolicyBenchmark:
    def __init__(self, data):
        self.data = data

    def parseData(self):
        _columns = self.data.columns
    
    def get_policy_benchmark(self, class_id):
        return self.data[self.data[POLICY_ID_COL] == class_id]