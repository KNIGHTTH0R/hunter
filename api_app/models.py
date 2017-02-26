"""Api`s models"""
import json
from bot.models import IITCRbotModel


class HunterModel(object):
    """Achieve Model, action: hunter"""
    def __init__(self, *args):
        self.data = args[0]
        self.current_user = args[1]

        self.team = self.data.get('team', 2)
        self.zoom = self.data.get('zoom', 10)
        self.coordinates = [self.data.get('late6'), self.data.get('lnge6')]

        self.days = int(self.data.get('days', 60))

        self.user_checked = self.data.get('user_checked')

        if self.days < 60:
            self.days = 60

        if self.zoom < 9:
            self.zoom = 9

        if not self.data.get('late6'):
            self.coordinates = []

        if self.data.get('latlng'):
            self.coordinates = self.data.get('latlng')

        self.arguments = {
            'latlng': self.coordinates,
            'days': self.days,
            'team': self.team,
            'zoom': self.zoom,
            'attention': self.attention(),
            'user_checked': self.user_checked
        }
        # self.arguments = self.data
        self.result = {
            # 'user': self.current_user,
            'args': self.data
        }

    def attention(self):
        import bot.util as util
        attention = None
        if self.data.get('attention'):
            attention = {
                'min_87': util.TimeCl().past_from_days(87),
                'max_87': util.TimeCl().past_from_days(91),
                'min_147': util.TimeCl().past_from_days(147),
                'max_147': util.TimeCl().past_from_days(151)
            }

        return attention

    def player(self):
        return self.data.get('player')

    def latlng(self):
        return self.coordinates

    def user(self):
        return {'result': self.current_user}

    def to_render_json(self, jdata):
        a = []
        hide = None
        data = {}
        for i in jdata:
            if i.get('showed'):
                hide = 'Some achievements was hidden by owner'
            else:
                a.append(i)
        self.result.update({'achievements': a})
        if hide:
            self.result.update({'hidden': hide})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class PlayerInfoModel(HunterModel):
    """Actions model, request 'search_player'"""
    def to_render_json(self, jdata):
        data = {}
        self.result.update({'player_info': jdata})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class ActionsModel(HunterModel):
    """Actions model, request 'search'"""
    def to_render_json(self, jdata):
        a = []
        data = {}
        for i in jdata:
            a.append(i)
        self.result.update({'actions': a})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class PortalModel(HunterModel):
    """Actions model, request 'search'"""
    def to_render_json(self, jdata):
        a = []
        data = {}
        for i in jdata:
            a.append(i)
        self.result.update({'portal': a})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class IITCModel(HunterModel):
    """Actions model, request 'iitc'"""
    def to_render_json(self, jdata):
        a = []
        data = {}
        for i in jdata:
            a.append(IITCRbotModel(i).data)
        data.update({'result': a})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class AdminModel(HunterModel):
    """Actions model, request 'super'"""
    def to_render_json_userlog(self, jdata):
        a = []
        data = {}
        for i in jdata:
            a.append(i)
        self.result.update({'userlog': a})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    def to_render_json_status(self, jdata):
        a = []
        data = {}
        for i in jdata:
            a.append(i)
        self.result.update({'status': a})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class ProfileModel(HunterModel):
    """Actions model, request 'profile'"""
    def to_render_json(self, jdata):
        data = {}
        self.result.update({'profile': jdata})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class PortalHistoryModel(HunterModel):
    """Actions model, request 'portal_history'"""
    def to_render_json(self, jdata):
        data = {}
        self.result.update({'portal_history': jdata})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class PlayerModel(HunterModel):
    """Actions model, request 'search_player'"""
    def to_render_json(self, jdata):
        data = {}
        self.result.update({'players': jdata})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class PlayerFromModel(HunterModel):
    """Actions model, request 'player_from'"""
    def to_render_json(self, jdata):
        data = {}
        self.result.update({'player_from': jdata})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class MonitorModel(HunterModel):
    """Actions model, request 'player_from'"""
    def to_render_json(self, jdata):
        data = {}
        self.result.update({'monitor': jdata})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class AccountModel(HunterModel):
    """Actions model, request 'accounts'"""
    def to_render_json(self, jdata):
        data = {}
        self.result.update({'accounts': jdata})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class InventoryModel(HunterModel):
    """Actions model, request 'inventory'"""
    def to_render_json(self, jdata):
        data = {}
        self.result.update({'items': jdata})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


class PortalDetailModel(HunterModel):
    """Actions model, request 'sofa'"""
    def to_render_json(self, jdata):
        data = {}
        self.result.update({'sofa': jdata})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    def to_render_json_history(self, jdata):
        data = {}
        self.result.update({'history': jdata})
        data.update({'result': self.result})
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))