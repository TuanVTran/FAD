import pandas as pd

class PolicyBenchmark:
    def __init__(self, data):
        self.data = data

    def parseData(self):
        _columns = self.data.columns
    
    def get_policy_benchmark(self, class_id):
        return self.data[self.data['Policy ID'] == class_id]