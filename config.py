import os
from enums import Env

# Default Values
ENV = Env.Production
SECRET_KEY = '72cowDH%FeJpqxX7*YXV'
DASHBOARD_PASSWORD = 'admin'
YTDL_CHECK_UPDATE_INTERVAL = 86400 #seconds - 86400: one a day

def config_get_env():
    try:
        if os.environ['ENV'] == 'dev':
            return Env.Development
        else:
            return ENV
    except:
        return ENV

def config_get_secret_key():
    try:
        return os.environ['SECRET_KEY']
    except:
        return SECRET_KEY

def config_get_dashboard_password():
    try:
        return os.environ['DASHBOARD_PASSWORD']
    except:
        return DASHBOARD_PASSWORD

def config_get_ytdl_check_update_interval():
    try:
        return int(os.environ['YTDL_CHECK_UPDATE_INTERVAL'])
    except:
        return YTDL_CHECK_UPDATE_INTERVAL