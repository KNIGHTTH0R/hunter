import json

import settings
import requests
from db.postgredb import PortalDetail
from telegram_bot.models import TelPortalDetailModel, TelegramMessageModel, guards


class TelegramController:
    def __init__(self, obj):
        self.obj = obj
        self.chat_id = obj.message.chat.id
        self.text = obj.message.text
        self.token = settings.TELEGRAM_TOKEN

        if self.chat_id < 0:
            self.is_group = True
            self.username = obj.message.chat.title
            self.message = 'Group '
        else:
            self.username = obj.message.chat.username
            self.is_group = False
            self.message = 'User '

    def executor(self):
        SendMessage(self.chat_id).sendChatAction()
        TelegramRequestController(self.obj).result()

    def start(self):
        self.sendMessage(self.message + 'is approved', self.chat_id)

    def sendMessage(self, message, chat_id):
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(self.token)
        payload = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
        requests.post(url, data=payload)


class SofaAchtungController(object):
    def __init__(self, portal_from_intel, diff, portaldb):
        self.portal_from_intel = portal_from_intel
        diff.update({'team': self.portal_from_intel['team']})
        self.diff = diff
        self.portaldb = portaldb
        self.parameters = None
        if self.portaldb.get('parameters'):
            self.parameters = self.portaldb.get('parameters').split(',')
        self.allow = None
        if self.portaldb.get('allow'):
            self.allow = self.portaldb.get('allow')
        self.tag = self.portaldb.get('tag')
        self.send_achtung()

    def send_achtung(self):
        parameters_set = {
            'hack': self.hackability(),
            'lvl': self.lvl(),
            'team': self.team(),
            '8': self.eight()
        }

        if not self.parameters:
            return

        for i in self.parameters:
            if not i:
                return
            if i == 'any':
                self.send_pd_telegram(self.tag)
                return

            if parameters_set[i]:
                self.send_pd_telegram(self.tag)
                return

    def hackability(self):
        if 'Multi-hack' in str(self.diff):
            return True
        elif 'Heat Sink' in str(self.diff):
            return True
        else:
            return False

    def lvl(self):
        if self.portaldb.get('lvl') != self.portal_from_intel.get('lvl'):
            return True

    def team(self):
        if self.portaldb.get('team') != self.portal_from_intel.get('team'):
            return True

    def eight(self):
        if self.portal_from_intel.get('lvl') == 8:
            return True

    def send_pd_telegram(self, tag):
        if not self.allow:
            return
        send_to = PortalDetail().get_allow_telegram_users(self.allow)

        for chat_id in send_to:
            if tag == 'diff':
                SendMessage(chat_id, TelPortalDetailModel(self.diff, self.portaldb, self.portal_from_intel
                                                          ).parse_diff()).sendMessageHard()
            elif tag == 'all':
                SendMessage(chat_id, TelPortalDetailModel(self.diff, self.portaldb, self.portal_from_intel
                                                          ).sofa(get_one=True)).sendMessageHard()


class GuardTelegram(object):
    def __init__(self, argument, user):
        if argument:
            self.request = {'request': 'player', 'player': argument, 'user': user}

            response = RequestApiController(self.request).result()
            if response and not response.get('error'):
                self.result = guards(response)
            else:
                self.result = response.get('error')
        else:
            self.result = argument


class HelpTelegram(object):
    def __init__(self, argument, user):
        self.result = 'a "agent name" - show achievements of agent.\n' \
                      '/help - this menu\n '


class TelegramRequestController(object):
    actions = {
            # 'ping': PingProfile,
            'a': GuardTelegram,
            # 'history': HistoryTelegram,
            # 'portal': PortalHistoryTelegram,
            # 'live': PlayerFromTelegram,
            # 'player': PlayerSearchTelegram,
            '/help': HelpTelegram,
            '/start': HelpTelegram,
            # 'monitor': MonitorTelegram
        }
    controller = None

    def __init__(self, data):
        self.message = TelegramMessageModel(data)
        self.chat_id = self.message.chat_id
        self.action = self.message.action()
        self.argument = self.message.argument()
        self.user = 'ass'
        if self.action in self.actions:
            self.controller = self.actions[self.action](self.argument, self.user)

    def result(self):
        if self.controller:
            counter = 0
            text = ''
            if len(self.controller.result) < 3800:
                SendMessage(self.chat_id, self.controller.result).sendMessage()
            else:
                for i in self.controller.result.split('\n'):
                    counter += len(i)
                    text += i+'\n'
                    if counter > 3800 or not len(i):
                        SendMessage(self.chat_id, text).sendMessage()
                        text = ''
                        counter = 0
            return self.controller.result
        return


class RequestApiController(object):
    """Telegram bot controller"""
    def __init__(self, request):
        self.headers = {
            'accept-encoding': 'gzip, deflate',
            'content-type': 'application/json; charset=UTF-8',
        }
        self.url = settings.TELEGRAM_URL
        self.token = settings.TOKEN_API
        request.update({'token': self.token})
        self.request = request

    def result(self):
        request = requests.post(self.url, data=json.dumps(self.request), headers=self.headers)
        return request.json()


class SendMessage(object):
    def __init__(self, chat_id, msg=None):
        self.chat_id = chat_id
        self.msg = msg

    """message* - portal detailed from intel"""
    def sendMessage(self):
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(settings.TELEGRAM_TOKEN)
        payload = {'chat_id': self.chat_id, 'text': self.msg, 'parse_mode': 'HTML', 'disable_web_page_preview': True}
        requests.post(url, data=payload)

    def sendMessageHard(self):
        url = 'https://api.telegram.org/bot_ID/sendMessage'
        payload = {'chat_id': self.chat_id, 'text': self.msg, 'parse_mode': 'HTML', 'disable_web_page_preview': True}
        requests.post(url, data=payload)

    def sendChatAction(self):
        url = 'https://api.telegram.org/bot{}/sendChatAction'.format(settings.TELEGRAM_TOKEN)
        payload = {'chat_id': self.chat_id, 'action': 'TYPING'}
        requests.post(url, data=payload)