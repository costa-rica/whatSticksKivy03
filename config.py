import os
import json

if os.environ.get('COMPUTERNAME')=='CAPTAIN2020':
    with open(r'C:\Users\captian2020\Documents\config_files\config_whatSticksApi02.json') as config_file:
        config = json.load(config_file)
elif os.environ.get('TERM_PROGRAM')=='Apple_Terminal':
    with open('/Users/nick/Documents/config_files/whatSticks.json') as config_file:
        config = json.load(config_file)
else:
    with open('/home/ubuntu/environments/config.json') as config_file:
        config = json.load(config_file)



class Config:
    DEBUG = True
    SECRET_KEY = config.get('SECRET_KEY')
    # SECRET_KEY='thisissecret'
    # SQLALCHEMY_DATABASE_URI='sqlite:///D:\\databases\\whatSticksApi02\\whatSticks.db'
    SQLALCHEMY_DATABASE_URI = config.get('SQL_URI_WHAT_STICKS')
    # APP_PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))
    # isExist = os.path.exists(APP_PACKAGE_DIR)
    # if not isExist:
    #     os.makedirs(APP_PACKAGE_DIR)
    # LOGS_DIR = os.path.join(APP_PACKAGE_DIR, '_logs')

    SQLALCHEMY_TRACK_MODIFICATIONS = True