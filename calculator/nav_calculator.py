
class NAVCalculator:
   def __init__(self):
      pass

   def get_end_nav(self, begin_nav, benchmark_return, flow_fd, start_date, end_date):
      # calculate end_nav with begin nav and benchmark_return
      # end_nav = begin_nav * ( 1 + benchmark) * Sum(from 1 to n) (Flow(i) * (1 + benchmark * ((T - t(i))/T) ))
      flow_cal_fd = flow_fd.copy()
      total_day = (end_date - start_date).days
      flow_cal_fd['FlowSum'] = flow_fd['value'] * (1 + benchmark_return * (total_day - (flow_cal_fd['date'] - start_date).dt.days)/total_day)
      flow_cal_fd['cumulative_flow'] = flow_cal_fd['FlowSum'].cumsum()
      total_flow = 0 if flow_cal_fd['cumulative_flow'].size == 0 else flow_cal_fd['cumulative_flow'].iloc[-1]
      end_nav = begin_nav * ( 1 + benchmark_return) + total_flow
      return end_nav

   def get_estimated_end_nav(self, begin_nav, benchmark_return, weight_cash_flow):
      return (begin_nav + weight_cash_flow) * ( 1 + benchmark_return)
