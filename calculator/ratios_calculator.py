import finance_calculator as fc

class RatiosCalculator:
   def __init__(self):
      pass
   
   def get_beta(self, nav_data, benchmark_data, windowSize=250):
      return fc.get_beta(nav_data, benchmark_data, window=windowSize)

   def get_alpha(self, nav_data, benchmark_data, windowSize=250):
      return fc.get_alpha(nav_data, benchmark_data, windowSize)

   