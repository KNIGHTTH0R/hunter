"Scanner cookies updater"
import json
import sys
sys.path.append('./')

import time
import requests
from db.redisdb import RedisCookiesModule
from db.postgredb import PCookies
from bot.util import TimeCl


def oauth_key(parameter):
    url = 'https://android.clients.google.com/auth'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'device': '3826c8a11a4e0165',
        'app': 'com.nianticproject.ingress',
        'User-Agent': 'GoogleAuth/1.4 (cancro MMB29M); gzip',
    }
    request = requests.post(url, data=parameter, headers=headers)
    print(request.text)
    for i in request.text.split('\n'):
        if 'Error' in i:
            return
        if 'Auth' in i:
            return i[5:]


def get_scan_cookie(parameter):
    if parameter:
        url = 'https://m-dot-betaspike.appspot.com/_ah/login'
        myparams = {'continue': 'https%3A%2F%2Fm-dot-betaspike.appspot.com', 'auth': parameter}
        resp = requests.get(url, params=myparams, allow_redirects=False)
        cookie = resp.headers['Set-Cookie'].split(';')[0]
        print(cookie)
        return cookie


def get_token(cookie, software):
    """GET XCSRF"""

    url = 'https://m-dot-betaspike.appspot.com/handshake'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Encoding': 'gzip',
        'Cookie': cookie,
        'User-Agent': 'Nemesis (gzip)',
    }

    request = requests.post(url, data=software, headers=headers)
    response = json.loads(request.text[5:])

    return response['result']['xsrfToken']


def main():
    while True:
        cookies_list = PCookies().get_scanner_cookies()
        for i in cookies_list:
            if TimeCl(i['slastupdate']).daydiff() > 0:
                parameter = i['additional_info']
                software = i['software']
                cookie = get_scan_cookie(oauth_key(parameter))
                token = get_token(cookie, software)
                cookies = '{}; {}'.format(cookie, token)
                PCookies().insert_scanner_cookie(cookies, i['email'])
                RedisCookiesModule().load_cookies()

        time.sleep(100)

if __name__ == '__main__':
    main()
