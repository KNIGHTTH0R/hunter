import argparse

COM_SLEEP = 0.01

INSPECTOR_SLEEP = 10

ACHIEVE_DAYS = 10

TOKEN_API = 'YOUR_TOKEN_HERE'

TELEGRAM_URL = 'https://ingress-guard.tk/api'

REDIS_PORT = 6379

parser = argparse.ArgumentParser(description='IngressGuard arguments')
parser.add_argument('--server_name', default='test', type=str, help='server name')
parser.add_argument('--redis_host', default='localhost', type=str, help='redis hostname')
args = parser.parse_args()

SERVER_NAME = args.server_name
REDIS_HOST = args.redis_host

DEBUG = True

if DEBUG:
    google_redirect_url = 'http://localhost:8888/auth/login/'
else:
    google_redirect_url = 'https://ingress-guard.tk/auth/login/'


PSQL_PRIMARY = 'dbname=hunter user=hunter password=password host=localhost port=5432'
PSQL_SECONDARY = 'dbname=hunter user=hunter password=password host=localhost port=5432'

LOG_FILE = './error_log'

if DEBUG:
    GOOGLE_KEY = ''
    GOOGLE_SECRET = ''
else:
    GOOGLE_KEY = ''
    GOOGLE_SECRET = ''

TELEGRAM_TOKEN = ""

from settings_local import *
