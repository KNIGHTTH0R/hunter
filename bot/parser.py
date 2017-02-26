import time

import collections
import json_delta
import json
import re

from bot.models import PortalModel, IntelPortalModel, IITCModel, PortalDetailDiffModel, IITCRbotModel, \
    ProfileScannerModel, TilePortalsModel, InventoryModel
import bot.util as util
from db.postgredb import ActionsLog, AchieveLog, PortalDetail, ScannerPg, PlayerPg
from db.redisdb import RedisCookiesModule, IITCLogModule, RedisLogModule, RedisActionsLogModule, TilesLogModule, \
        PlayerLogModule, RedisSubscription
from bot.bot import Intel, Scanner
from telegram_bot.controller import SofaAchtungController


class CommPreParser(object):
    def __init__(self, result):
        # actions_args = []
        player_args = []
        achieve_args = []
        ada_destroed = []

        for query in result['result']:
            self.result = query

            if query[2].get('plext').get('plextType') == "SYSTEM_BROADCAST": 
                actions_query = PortalModel(self.result).actions
                player_name = actions_query.get('player')
                timestamp = actions_query.get('timestamp')
                player_args.append(actions_query)

                if actions_query['plain'] == 2:
                    achieve_query = PortalModel(self.result).achieve
                    if achieve_query not in achieve_args:
                        achieve_args.append(achieve_query)

                if actions_query['plain'] == 3:
                    ada_destroed.append(PortalModel(self.result).achieve)

        ada_detected = util.ada_execute(ada_destroed)
        if ada_detected:
            for query in ada_detected:
                query.update({'ada': True})
                achieve_args.append(query)
        RedisLogModule().log_achive_query(achieve_args)
        PlayerLogModule.log_query(player_args)


class CommParser(object):
    def __init__(self, query):
        self.query = query

    def actions_parser(self):
        actions_args = []
        actions_keys = None
        for query in self.query:
            result = json.loads(query.decode('UTF-8'))
            actions_keys = tuple(sorted(result))
            actions_args.append(tuple(map(lambda key: result[key], sorted(result.keys()))))

        ActionsLog().insert_comm(str(actions_keys).replace('\'', ''), actions_args)

    def player_parser(self):
        player_args = []
        player_keys = None
        counter = 0
        for query in self.query:
            counter += 1
            result = json.loads(query.decode('UTF-8'))
            result.pop('mguid')
            player_keys = tuple(sorted(result))
            player_args.append(tuple(map(lambda key: result[key], sorted(result.keys()))))
            if counter == 50:
                ActionsLog().insert_player(str(player_keys).replace('\'', ''), player_args)
                counter = 0
                player_args = []
                player_keys = []

    def achive_parser(self):
        achive_args = []
        achive_keys = None
        latlng_list = []
        for query in reversed(self.query):
            result = json.loads(query.decode('UTF-8'))
            result.update({'showed': False})
            latlng = (result['late6'], result['lnge6'])
            if latlng not in latlng_list:
                latlng_list.append(latlng)
                achive_keys = tuple(sorted(result))
                achive_args.append(tuple(map(lambda key: result[key], sorted(result.keys()))))

        try:
            AchieveLog().insert_achive(str(achive_keys).replace('\'', ''), achive_args)
        except Exception as e:
            for i in achive_args:
                AchieveLog().insert_achive(str(achive_keys).replace('\'', ''), (i,))

    def subscribe(self):
        for query in reversed(self.query):
            result = json.loads(query.decode('UTF-8'))
            pub = {
                'late6': result.get('late6'),
                'lnge6': result.get('lnge6'),
                'player': result.get('player'),
                'team': result.get('team'),
                'address': result.get('address'),
                'name': result.get('name')
            }
            RedisSubscription.pub_log(json.dumps(pub))


class PortalDetailParser(object):
    def __init__(self, guid):
        self.guid = guid
        cookie = RedisCookiesModule().get_cookie()
        if cookie:
            intel = Intel(cookie)
            self.portal = intel.fetch_portal(self.guid)

    def get_portal_details(self):
        result = IntelPortalModel(self.guid, self.portal['result']).data
        if result.get('team'):
            self.update_achive()
            return result
        return {'error': 'can`t fetch portal from intel'}

    def update_achive(self):
        upd = []
        result = IntelPortalModel(self.guid, self.portal['result']).achieve
        if result['team'] == 3:
            result.update({'timestamp': int(round(time.time() * 1000))})
            update_arg = tuple(sorted(result))
            upd.append(tuple(map(lambda key: result[key], sorted(result.keys()))))
            AchieveLog().insert_achive(str(update_arg).replace('\'', ''), upd)


class IITCParser:
    def to_redis(self, portal):
        self.portal = IITCModel(portal).data
        if self.portal['data'].get('title'):
            IITCLogModule().log_query(self.portal)

    def to_postgres(self, query_list):
        achieve_args = []
        neutrals = []
        achieve_keys = None
        neutral_keys = None

        for query in query_list:
            self.result = json.loads(query.decode('UTF-8'))
            portal = IITCModel(self.result).iitc_achive
            query = IITCModel(self.result).update
            if portal.get('team') == 3:
                neutral_keys = tuple(sorted(portal))
                nvalue = tuple(map(lambda key: portal[key], sorted(portal.keys())))
                if nvalue not in neutrals:
                    neutrals.append(nvalue)
            else:
                achieve_keys = tuple(sorted(query))
                value = tuple(map(lambda key: query[key], sorted(query.keys())))
                if value not in achieve_args:
                    achieve_args.append(value)
            AchieveLog().insert_iitc_guid(str(achieve_keys).replace('\'', ''), achieve_args)
            AchieveLog().insert_iitc_achive(str(neutral_keys).replace('\'', ''), neutrals)


class PortalParser(object):
    def __init__(self, portaldb, result_from_intel):

        self.result_from_intel = IntelPortalModel(portaldb['guid'], result_from_intel).for_diff

        diff = json_delta.load_and_diff(json.dumps(PortalDetailDiffModel.portal_for_diff(portaldb)),
                                        json.dumps(PortalDetailDiffModel.portal_for_diff(self.result_from_intel)),
                                        verbose=False)

        if diff:
            diff_data = {}
            for i in diff:
                try:
                    diff_data.update({
                        i[0][0]: i[1]
                    })
                except:
                    print('exception')

            """Update PD in database"""
            PortalDetail().update_pd(self.result_from_intel)
            try:
                """Send information to telegram"""
                SofaAchtungController(self.result_from_intel, diff_data, portaldb)
            except Exception as e:
                print(e)


class ProfileScannerParser(object):
    def get_profile(self, player, user=None):
        if not player or len(player) > 15 or len(player.split()) != 1:
            return {'error': 'name not matched'}
        force = False

        if player.endswith('!'):
            player = player[:-1]
            force = True

        profile = ScannerPg().get_profile(player)

        if profile and not force:
            if util.TimeCl(profile['update']).daydiff() < 3:
                return profile

        profile = Scanner().get_player_profile(player, user)
        if profile.get('error'):
            return profile
        if not profile.get('ap') or profile.get('error'):
            ScannerPg().insert_error_profile(player)
            return {'error': 'Player profile not found, banned or renamed', 'playername': player}

        ScannerPg().insert_profile(ProfileScannerModel(profile).profile)

        return ProfileScannerModel(profile).profile


class InventoryScannerParser:
    def __init__(self, data, path, headers):

        if path == '/rpc/playerUndecorated/getInventory':
            self.headers = headers
            self.data = json.loads(data.decode('UTF-8'))
            self.get_inventory()
        elif path == '/handshake':
            self.data = json.loads(data.decode('UTF-8')[5:])
            self.get_user()

    def get_inventory(self):
        for i in self.headers:
            if i == 'Cookie':
                cookie = self.headers[i]
            elif i == 'X-XsrfToken':
                xsrf = self.headers[i]
        ScannerPg().update_agent_cookies(cookie, xsrf)

        inventory = self.data.get('gameBasket').get('inventory')
        agent_id = ''
        if inventory:
            resourceWithLevels = collections.OrderedDict()
            resource = collections.OrderedDict()
            modResource = collections.OrderedDict()
            portalkeys = []

            for i in inventory:
                if agent_id == '':
                    agent_id = i[2].get('inInventory').get('playerId')
                rw = i[2].get('resourceWithLevels')
                r = i[2].get('resource')
                rm = i[2].get('modResource')
                capsule = i[2].get('container')

                if rw:
                    item = '{}_{}'.format(rw['level'], rw['resourceType'])
                    if item not in resourceWithLevels:
                        resourceWithLevels[item] = 1
                    else:
                        counter = resourceWithLevels[item]
                        resourceWithLevels[item] = counter + 1

                elif r:
                    if r.get('resourceType') == 'PORTAL_LINK_KEY':
                        portalKey = i[2].get('portalCoupler')
                        lat, lng = portalKey.get('portalLocation').split(',')
                        late6 = int('0x{}'.format(lat[1:]), 16)
                        lnge6 = int('0x{}'.format(lng[1:]), 16)
                        portalKey.update({'portalLocation': [late6, lnge6]})
                        portalkeys.append(portalKey)
                    elif r.get('resourceType') == 'FLIP_CARD':
                        item = '{}_{}'.format(r['resourceType'], i[2]['flipCard']['flipCardType'])

                        if item not in resource:
                            resource[item] = 1
                        else:
                            counter = resource[item]
                            resource[item] = counter + 1

                    else:
                        item = '{}_{}'.format(r['resourceType'], r['resourceRarity'])

                        if capsule:
                            if item not in resource:
                                resource[item] = 1
                            else:
                                counter = resource[item]
                                resource[item] = counter + 1
                            for items in capsule.get('stackableItems'):
                                az = items.get('exampleGameEntity')[2]
                                res = az.get('resource')
                                resw = az.get('resourceWithLevels')
                                resm = az.get('modResource')

                                if res:
                                    if res.get('resourceType') == 'PORTAL_LINK_KEY':
                                        portalKey = az.get('portalCoupler')
                                        lat, lng = portalKey.get('portalLocation').split(',')
                                        late6 = int('0x{}'.format(lat[1:]), 16)
                                        lnge6 = int('0x{}'.format(lng[1:]), 16)
                                        portalKey.update({'portalLocation': [late6, lnge6]})
                                        portalkeys.append(portalKey)
                                    elif res.get('resourceType') == 'FLIP_CARD':
                                        item = '{}_{}'.format(res['resourceType'], az['flipCard']['flipCardType'])
                                        count = capsule.get('currentCount')
                                        if item not in resource:
                                            resource[item] = count
                                        else:
                                            counter = resource[item]
                                            resource[item] = counter + count
                                    else:
                                        item = '{}_{}'.format(res['resourceType'], res['resourceRarity'])
                                        count = capsule.get('currentCount')
                                        if item not in resource:
                                            resource[item] = count
                                        else:
                                            counter = resource[item]
                                            resource[item] = counter + count
                                elif resw:
                                    item = '{}_{}'.format(resw['level'], resw['resourceType'])
                                    count = capsule.get('currentCount')
                                    if item not in resourceWithLevels:
                                        resourceWithLevels[item] = count
                                    else:
                                        counter = resourceWithLevels[item]
                                        resourceWithLevels[item] = counter + count
                                elif resm:
                                    item = '{}_{}'.format(resm['resourceType'], resm['rarity'])
                                    count = capsule.get('currentCount')
                                    if item not in modResource:
                                        modResource[item] = count
                                    else:
                                        counter = modResource[item]
                                        modResource[item] = counter + count
                        else:
                            if item not in resource:
                                resource[item] = 1
                            else:
                                counter = resource[item]
                                resource[item] = counter + 1
                elif rm:
                    item = '{}_{}'.format(rm['resourceType'], rm['rarity'])
                    if item not in modResource:
                        modResource[item] = 1
                    else:
                        counter = modResource[item]
                        modResource[item] = counter + 1

            itogo = {
                'resourceWithLevels': resourceWithLevels,
                'resource': resource,
                'modResource': modResource,
                'portalKeys': portalkeys
            }
            ScannerPg().update_agent_inventory(itogo, agent_id)

    def get_user(self):
        result = self.data.get('result')
        entity = result.get('playerEntity')[2]
        agent_name = result.get('nickname')
        xsrf = result.get('xsrfToken')
        faction = entity.get('controllingTeam').get('team')
        agent_id = result.get('playerEntity')[0]
        ScannerPg().update_agent_info(agent_name, agent_id, xsrf, faction)


class PortalHistoryParser(object):
    def __init__(self, data):
        self.url = data.get('url')
        self.late6 = data.get('late6')
        self.lnge6 = data.get('lnge6')

    def get_portal_history(self):
        if self.url and 'ingress.com/intel' in self.url:
            latlng = re.search(r'pll=(\d+\.\d+),(\d+\.\d+)', self.url).groups()
            self.late6 = int(float(latlng[0])*1E6)
            self.lnge6 = int(float(latlng[1])*1E6)
        if not self.late6 or not self.lnge6:
            return {'error': 'invalid url or coordinates'}

        return PortalDetail().portal_history(self.late6, self.lnge6)


class MonitorParser(object):
    def __init__(self, data):
        self.url = data.get('url')
        self.late6 = data.get('late6')
        self.lnge6 = data.get('lnge6')

    def add_portal_to_monitor(self):
        if self.url and 'ingress.com/intel' in self.url:
            latlng = re.search(r'pll=(\d+\.\d+),(\d+\.\d+)', self.url).groups()
            self.late6 = int(float(latlng[0])*1E6)
            self.lnge6 = int(float(latlng[1])*1E6)
            try:
                portal = AchieveLog().get_portal_by_latlng(self.late6, self.lnge6)[0]
                PortalDetail().add_pd_portal(portal)
                return portal
            except:
                return {'error': 'not found in base, can`t add'}

        if not self.late6 or not self.lnge6:
            return {'error': 'invalid url or coordinates'}


class PlayerParser(object):
    def get_player_from(self, player):
        result = PlayerPg().player_from(player.lower())
        if result:
            return result
        if not result:
            result = util.UserStatistics().create_statistics(player)
            return result
        return {'error': 'User not found in base!'}


class TilesParser(object):
    def __init__(self, result):
        self.result = result.get('result')

    def get_portals(self):
        statuses = []

        if self.result.get('map'):
            tiles = self.result['map']
            for i in tiles:
                if (tiles[i]).get('error'):
                    statuses.append({'tile': i, 'status': 'error'})
                elif (tiles[i]).get('gameEntities'):
                    statuses.append({'tile': i, 'status': 'exist'})
                    portal = self.parse_true_tiles((tiles[i]).get('gameEntities'), i)
                    if portal:
                        TilesLogModule().log_query(portal)

    def parse_true_tiles(self, tile_result, tile):
        portals = []
        for i in tile_result:
            "Filter portals"
            result = i[2]

            if result[0] == 'p':
                portals.append(TilePortalsModel(i, tile).portal)

        return portals

    def from_redis_to_psql(self, values):
        if not values:
            return

        portals = []

        for i in values:
            portals.append(json.loads(i.decode('UTF-8')))
        AchieveLog().tile_update_portals(portals)
