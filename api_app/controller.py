import functools
import json

from tornado.web import HTTPError
import settings
from db.postgredb import ActionsLog, AchieveLog, Admin, PlayerPg, PortalDetail, ScannerPg
from api_app.models import HunterModel, PlayerModel, ActionsModel, IITCModel, AdminModel, ProfileModel, PortalHistoryModel, \
    PlayerModel, PlayerFromModel, PortalDetailModel, MonitorModel, PortalModel, PlayerInfoModel, \
    AccountModel, InventoryModel
from bot.parser import PortalDetailParser, ProfileScannerParser, PortalHistoryParser, PlayerParser, MonitorParser
from bot.util import daemon_statistic


def is_super_action(action):
    action_list = ['super', 'status']
    if action in action_list:
        return True


def user_logger(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            Admin().write_user_log(self.request, self.current)
        except:
            pass
        return func(self, *args, **kwargs)
    return wrapper


class AdminController(object):
    """Admin Controller, action: super"""
    def __init__(self, data, current):
        hm = AdminModel(data, current)
        self.render = hm.to_render_json_userlog(Admin().get_user_log())


class SearchController(object):
    """Search Player Controller, action: search"""
    def __init__(self, data, current):
        hm = ActionsModel(data, current)
        player = hm.player()
        if player and len(player) > 2:
            self.render = hm.to_render_json(ActionsLog().find_player_actions(player))
        else:
            self.render = {'error': 'short name'}


class HunterController(object):
    DESCRIPTION = '{"request": "achievements", #required\n' \
                  '"late6":34010550, #required\n' \
                  '"lnge6": -118.085861, #required\n' \
                  '"days": 100, #default 60\n' \
                  '"team": 1, #default 2' \
                  '"zoom": 9, #default 9, min zoom 9' \
                  '"attention": true #default null}' \
                  '"user_checked": true #default false'
    """Achievements Controller, action: achievements"""
    def __init__(self, data, current):
        hm = HunterModel(data, current)

        if hm.latlng():
            self.render = hm.to_render_json(AchieveLog().get_achieve_by_latlng(hm.arguments))
        else:
            raise HTTPError(405, 'Bad arguments in request')


class PlayerController(object):
    DESCRIPTION = '{"player": "Test", #required\n' \
                  '"request": "player" #required}'
    """Player Controller, action: hunter"""
    def __init__(self, data, current):
        hm = HunterModel(data, current)
        self.player = hm.player()

        if self.player:
            self.render = hm.to_render_json(AchieveLog().get_achieve_by_player(hm.result))
        else:
            raise HTTPError(405, 'Bad arguments in request')


class PlayerInfoController(object):
    DESCRIPTION = '{"request": "player_info", #required' \
                  '"player": "Test" #required}'
    """Player Controller, action: hunter"""
    def __init__(self, data, current):
        hm = PlayerInfoModel(data, current)
        self.player = hm.player()

        if self.player:
            self.render = hm.to_render_json(Admin().get_players(self.player))
        else:
            raise HTTPError(405, 'Bad arguments in request')


class StatusController(object):
    """Bot status controller, action: status"""
    def __init__(self, data, current):
        hm = AdminModel(data, current)
        self.render = hm.to_render_json_status(daemon_statistic())


class PortalController(object):
    DESCRIPTION = '{"request": "portal", #required\n' \
                  '"late6":34010550, #required\n' \
                  '"lnge6": -118085861 #required}'
    """Portal controller, action: portal"""
    def __init__(self, data, current):
        hm = PortalModel(data, current)
        if hm.latlng():
            self.render = hm.to_render_json(AchieveLog().get_portal_by_latlng(hm.latlng()))
        else:
            raise HTTPError(405, 'Bad arguments in request')


class PortalCheckController(object):
    def __init__(self, data, current):
        portaldata = data.get('portaldata')
        if portaldata:
            query = portaldata
            AchieveLog().insert_iitc_achieve_check(query)
            self.render = {'status': 'ok'}
        else:
            self.render = {'status': 'error'}


class IITC_portals(object):
    """IITC controller, action: iitc"""
    def __init__(self, data, current):
        hm = IITCModel(data, current)
        self.render = hm.to_render_json(AchieveLog().get_achieve_by_latlng(hm.arguments))


class ProfileController(object):
    def __init__(self, data, current):
        player = data.get('player')
        hm = ProfileModel(data, current)
        self.render = hm.to_render_json(ProfileScannerParser().get_profile(player, current.get('email')))


class PortalHistoryController(object):
    def __init__(self, data, current):
        hm = PortalHistoryModel(data, current)
        self.render = hm.to_render_json(PortalHistoryParser(data).get_portal_history())


class PlayerSearchController(object):
    def __init__(self, data, current):
        player = data.get('player')
        hm = PlayerModel(data, current)
        self.render = hm.to_render_json(PlayerPg().find_player(player))


class PlayerFromController(object):
    def __init__(self, data, current):
        player = data.get('player')
        hm = PlayerFromModel(data, current)
        self.render = hm.to_render_json(PlayerParser().get_player_from(player))


class MonitorController(object):
    def __init__(self, data, current):
        hm = MonitorModel(data, current)
        self.render = hm.to_render_json(MonitorParser(data).add_portal_to_monitor())


class AccountsController(object):
    def __init__(self, data, current):
        hm = AccountModel(data, current)
        self.render = hm.to_render_json(ScannerPg().get_user_accounts(current.get('email')))


class AccountAddController(object):
    def __init__(self, data, current):
        agent_name = data.get('agent_name')
        hm = AccountModel(data, current)
        self.render = hm.to_render_json(ScannerPg().add_account(agent_name, current.get('email')))


class AccountRemoveController(object):
    def __init__(self, data, current):
        agent_name = data.get('agent_name')
        hm = AccountModel(data, current)
        self.render = hm.to_render_json(ScannerPg().remove_account(agent_name, current.get('email')))


class AccountActiveController(object):
    def __init__(self, data, current):
        agent_name = data.get('agent_name')
        hm = AccountModel(data, current)
        self.render = hm.to_render_json(ScannerPg().remove_account(agent_name, current.get('email')))


class AccountHideController(object):
    def __init__(self, data, current):
        agent_id = data.get('agent_id')
        hm = AccountModel(data, current)
        self.render = hm.to_render_json(ScannerPg().hide_achievements(agent_id, current.get('email')))


class InventoryController(object):
    def __init__(self, data, current):
        agent_id = data.get('agent_id')
        hm = InventoryModel(data, current)
        self.render = hm.to_render_json(ScannerPg().get_agent_inventory(agent_id))


class ApiController(object):

    actions = {
        'achievements': HunterController,
        'player': PlayerController,
        'player_info': PlayerInfoController,
        'portal': PortalController,
        'portal_check': PortalCheckController,
        'get_profile': ProfileController,
        'accounts': AccountsController,
        'inventory': InventoryController,
        'add_account': AccountAddController,
        'account_remove': AccountRemoveController,
        'set_active': AccountActiveController,
        'hide': AccountHideController
        # 'status': StatusController,
        # 'iitc': IITC_portals,
        # 'super': AdminController,
        # 'profile': ProfileController,
        # 'portal_history': PortalHistoryController,
        # 'search_player': PlayerSearchController,
        # 'player_from': PlayerFromController,
        # 'monitor': MonitorController,
        # 'search': SearchController,
    }
    controller = None
    """main /api controller"""
    def __init__(self, data, current):
        self.current = current
        self.request = data
        self.action = data.get('request')
        # self.permissions = current.get('permissions').split(',')
        if self.action in self.actions:
            # if 'all' in self.permissions:
            self.controller = self.actions[self.action](data, current)
            # elif self.action in self.permissions:
            #     self.controller = self.actions[self.action](data, current)
            # elif 'not' in self.permissions:
            #     raise HTTPError(400, 'Request not allowed')
            # else:
            #     raise HTTPError(400, 'Request not allowed')
        else:
            raise HTTPError(400, 'Request not allowed')

    @user_logger
    def render(self):
        return self.controller.render


class UserController(object):
    def __init__(self):
        pass
