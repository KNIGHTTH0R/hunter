import sys
sys.path.append('./')

from telegram_bot.controller import TelegramController
from time import sleep

import requests
import settings
import json
import logging


class TelegramBot(object):
    message = ''
    update_id = ''


def as_bot(json_data):
    t = TelegramBot()
    t.__dict__.update(json_data)
    return t


class Telegram:
    def __init__(self):
        self.token = settings.TELEGRAM_TOKEN
        self.running = True
        self.last_update_id = 0

    def getUpdates(self, offset=None, limit=None, timeout=1):
        url = 'https://api.telegram.org/bot{}/getUpdates'.format(self.token)
        data = {'timeout': 0}
        if limit:
            data['limit'] = 1
        if offset:
            data['offset'] = self.last_update_id + 1

        return requests.post(url, data, timeout=timeout).json()['result']

    def start_polling(self, poll_interval, timeout=1):
        while self.running:
            try:
                updates = self.getUpdates(self.last_update_id, timeout=timeout)
            except:
                poll_interval += 1
            else:
                if updates:
                    for update in updates:
                        logging.warning(update)
                        try:
                            TelegramController(json.loads(json.dumps(update), object_hook=as_bot)).executor()
                        except:
                            pass
                    self.last_update_id = updates[-1]['update_id']

            sleep(poll_interval)



Telegram().start_polling(4)