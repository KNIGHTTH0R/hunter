import random
import requests
import requests.exceptions
import re
import json
# from json import JSONDecodeError
from bot.models import CookieModel, TaskModel
from db.redisdb import RedisSettingsModule, RedisCookiesModule
from db.postgredb import PCookies


class Intel(object):
    def __init__(self, cookies, task=None):
        self.id = CookieModel(cookies).id()
        self.headers = {
            'accept-encoding' :'gzip, deflate',
            'content-type': 'application/json; charset=UTF-8',
            'cookie': CookieModel(cookies).cookie(),
            'origin': 'https://www.ingress.com',
            'referer': 'https://www.ingress.com/intel',
            'user-agent': 'Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'x-csrftoken': CookieModel(cookies).token(),
        }
        if task:
            self.field = TaskModel(task).field()
        self.refresh_version()

    def refresh_version(self):
        self.version = RedisSettingsModule.version_control_get()
        if not self.version:
            request = requests.get('https://www.ingress.com/intel', headers=self.headers)
            RedisSettingsModule.version_control_set(re.findall(r'gen_dashboard_(\w*)\.js', request.text)[0])
            self.version = RedisSettingsModule.version_control_get()

    def fetch(self, url, payload):
        payload['v'] = self.version
        request = requests.post(url, data=json.dumps(payload), headers=self.headers, timeout=(20, 30))
        try:
            result = request.json()
        except Exception as e:
            result = {'error': 'cookies'}
        return result

    def fetch_msg(self, mints=-1, maxts=-1, reverse=False, tab='all'):
        url = 'https://www.ingress.com/r/getPlexts'
        payload = {
            'maxLatE6': self.field['maxLatE6'],
            'minLatE6': self.field['minLatE6'],
            'maxLngE6': self.field['maxLngE6'],
            'minLngE6': self.field['minLngE6'],
            'maxTimestampMs': maxts,
            'minTimestampMs': mints,
            'tab': tab
        }
        if reverse:
            payload['ascendingTimestampOrder'] = True
        return self.fetch(url, payload)

    def fetch_map(self, tilekeys):
        url = 'https://www.ingress.com/r/getEntities'
        payload = {
            'tileKeys': tilekeys
        }
        return self.fetch(url, payload)

    def fetch_portal(self, guid):
        url = 'https://www.ingress.com/r/getPortalDetails'
        payload = {
            'guid': guid
        }
        return self.fetch(url, payload)


class Scanner(object):
    def __init__(self):
        pass

    def get_player_profile(self, player, user):
        cookies = PCookies().get_user_scanner_cookies(user)

        if not cookies:
            return {'error': 'Connect via proxy first for update request info. You can find instruction on main site.'}
        else:
            cookie = cookies[0].get('cookie')
            token = cookies[0].get('xsrf')
            url = 'https://m-dot-betaspike.appspot.com/rpc/playerUndecorated/getPlayerProfile'
            headers = {
                'Content-Type': 'application/json; charset=UTF-8',
                'Cookie': cookie,
                'User-Agent': 'Nemesis (gzip)',
                'X-XsrfToken': token,
            }

            payloads = {"params": [player]}

            request = requests.post(url, data=json.dumps(payloads), headers=headers)
            try:
                if request.json().get('error'):
                    return {'error': "Agent name don`t exists, banned or renamed", 'playername': player}

                result = request.json()['result']
                result.update({'playername': player})
            except:
                return {'error': 'Please update credentials via proxy.'}

            return result

if __name__ == '__main__':
    pass
