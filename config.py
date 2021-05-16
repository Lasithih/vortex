import os
from enum import Enum

class Env(Enum):
    Production = 1
    Development = 2

# Default Values
ENV = Env.Production
SECRET_KEY = '72cowDH%FeJpqxX7*YXV'
DASHBOARD_PASSWORD = 'admin'

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