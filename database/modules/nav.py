
from ..model.nav import NAV

def find_nav_by_id(fund_id):
    return NAV.objects(id=fund_id)

def find_nav_by_title(tilte):
    return NAV.objects(title=tilte)