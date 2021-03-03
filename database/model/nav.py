from  mongoengine import *
import datetime
from fadgit.utils import utilities as utils
from fadgit.constant import configuration as constant
import json

class NAV(Document):
    # Meta variables.
    meta = {
        'db_alias': 'fad',
        'collection': 'nav'
    }

    # Document variables.
    # report_acc_number = StringField(required=True, max_length=200)
    # report_acc_name = StringField(max_length=200)
    # nav = IntField(required=True)
    # as_of_date = DateField()

class NAVReader():
    def __init__():
        pass

    @staticmethod
    def init_model_from_file(self):
        dir_path = utils.get_data_sample_dir_path()
        nav_df = utils.parseCSV(dir_path, constant.FUND_NAV_FILE)
        data_json = nav_df.to_dict(orient='records')
        for r in data_json:
            for k,v in r:
                nav_element = NAV()
                k = k.lower()
                k = '_'.join(k.split(' '))
                nav_element[k] = v
                nav_element.save()
    