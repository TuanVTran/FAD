
from .ratios_calculator import RatiosCalculator
from .nav_calculator import NAVCalculator

def get_end_nav(begin_nav, benchmark_return, flow_fd, start_date, end_date):
    return NAVCalculator().get_end_nav(begin_nav, benchmark_return, flow_fd, start_date, end_date)

def get_estimated_end_nav(begin_nav, benchmark_return, weight_cash_flow):
    return NAVCalculator().get_estimated_end_nav(begin_nav, benchmark_return, weight_cash_flow)

def get_beta(nav_data, benchmark_data, windowSize=250):
    return RatiosCalculator().get_beta(nav_data, benchmark_data, windowSize)

def get_alpha(nav_data, benchmark_data, windowSize=250):
    return RatiosCalculator().get_alpha(nav_data, benchmark_data, windowSize)