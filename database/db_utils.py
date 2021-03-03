from pprint import pprint
from config import config as cf
from mongoengine import *
from .model.nav import NAV, NAV
from .modules import nav as nav_mod

def connect_db():
    connection = connect(cf.config.dbName, host=cf.config.dbURI, alias=cf.config.alias)

def disconect_db():
    disconnect(alias=cf.config.alias)

def initialize_db():
    nav = NAV(report_acc_number='KSBG250NOT00',nav=1000)
    nav.save()