import json
import re
import time


class CookieModel(object):
    def __init__(self, cookies):
        self.cookies = cookies

    def email(self):
        return self.cookies.get('email')

    def id(self):
        return self.cookies.get('id')

    def status(self):
        return self.cookies.get('status')

    def cookie(self):
        return self.cookies['cookie'].strip()

    def token(self):
        return re.findall(r'csrftoken=(\w*);', self.cookie())[0]


class TaskModel(object):
    def __init__(self, tasks):
        self.tasks = tasks

    def task(self):
        return self.tasks['task']

    def latlng(self):
        return self.tasks['latlng']

    def status(self):
        return self.tasks['status']

    def field(self):
        latlng = self.latlng()
        field = {
            'minLngE6': round(latlng['minLngE6']),
            'minLatE6': round(latlng['minLatE6']),
            'maxLngE6': round(latlng['maxLngE6']),
            'maxLatE6': round(latlng['maxLatE6']),
        }
        return field


class PortalModel(object):
    "Portal object"
    def __init__(self, raw_msg):
        plains = {
            ' deployed a Resonator on ': 1,
            ' captured ': 2,
            ' destroyed a Resonator on ': 3,
            ' linked ': 4,
            ' created a Control Field @': 5,
            ' destroyed the Link ': 6,
            ' destroyed a Control Field @': 7,
            ' deployed a Portal Fracker on ': 8,
            ' deployed a Beacon on ': 9,

        }

        self.raw = raw_msg
        self.guid = raw_msg[0]
        self.timestamp = raw_msg[1]
        try:
            self.address = raw_msg[2]['plext']['markup'][2][1]['address']
        except:
            self.address = 'Unknown address'
            
        """ENLIGHTENED = 1, RESISTANCE = 2"""
        if raw_msg[2]['plext']['team'] == 'ENLIGHTENED':
            self.team = 1
        else:
            self.team = 2
        self.plain = plains[raw_msg[2]['plext']['markup'][1][1]['plain']]
        self.player = raw_msg[2]['plext']['markup'][0][1]['plain']
        self.latE6 = raw_msg[2]['plext']['markup'][2][1]['latE6']
        self.lngE6 = raw_msg[2]['plext']['markup'][2][1]['lngE6']
        self.portalname = raw_msg[2]['plext']['markup'][2][1]['name']
        """For actions"""
        self.actions = {'mguid': self.guid,
                        'player': self.player,
                        'timestamp': self.timestamp,
                        'team': self.team,
                        'late6': self.latE6,
                        'lnge6': self.lngE6,
                        'plain': self.plain,
                        'name': self.portalname,
                        'address': self.address,
        }
        """For achievements"""
        self.achieve = {'player': self.player,
                        'team': self.team,
                        'timestamp': self.timestamp,
                        'name': self.portalname,
                        'late6': self.latE6,
                        'lnge6': self.lngE6,
                        'address': self.address,
                        'ada': False,
                        'status': None
        }


class IntelPortalModel(object):
    "Portal info parser"
    def __init__(self, guid, raw_msg):
        self.raw_msg = raw_msg
        self.current_milli_time = int(round(time.time() * 1000))
        self.player = self.raw_msg[16]
        self.team = self.raw_msg[1]
        self.img = self.raw_msg[7]
        self.name = self.raw_msg[8]
        self.level = self.raw_msg[4]

        self.resonators = []
        for val in self.raw_msg[15]:
            self.resonators.append([val[0], val[1]])

        self.mods = []
        for val in self.raw_msg[14]:
            if val:
                self.mods.append([val[0], val[1], val[2]])
            else:
                self.mods.append(None)

        self.guid = guid
        self.timestamp = self.current_milli_time
        self.latE6 = self.raw_msg[2]
        self.lngE6 = self.raw_msg[3]
        if self.team == 'E':
            self.full_team = 1
        elif self.team == 'R':
            self.full_team = 2
        elif self.team == 'N':
            self.full_team = 3

        self.data = {
            'guid': self.guid,
            'name': self.name,
            'team': self.full_team,
            'player': self.player,
            'lvl': self.level,
            'resonators': {'res': self.resonators},
            'mods': {'mod': self.mods},
            'timestamp': self.timestamp,
            'img': self.img,
            'late6': self.latE6,
            'lnge6': self.lngE6
        }

        self.achieve = {
            'name': self.name,
            'late6': self.latE6,
            'lnge6': self.lngE6,
            'player': self.player,
            'team': self.full_team,
            'showed': self.timestamp,
            'img': self.img
        }
        
        self.for_diff = {
            'guid': self.guid,
            'name': self.name,
            'team': self.full_team,
            'player': self.player,
            'lvl': self.level,
            'resonators': self.resonators,
            'mods': self.mods,
            'late6': self.latE6,
            'lnge6': self.lngE6
        }


class PortalDetailDiffModel(IntelPortalModel):
    def diff_portal(self, portaldb):
        self.to_send = portaldb.get('allow')
        self.task = portaldb.get('task')
        diff = self.data
        diff.update({'task': self.task, 'allow': self.to_send})
        return diff


    @classmethod
    def portal_for_diff(cls, portal):
        if type(portal) is dict:
            for_diff = {
                'team': portal.get('team'),
                'player': portal.get('player'),
                'lvl': portal.get('lvl'),
                'resonators': portal.get('resonators'),
                'mods': portal.get('mods'),
            }
            return for_diff


class TilePortalsModel(object):
    def __init__(self, raw, tile):
        self.pguid = raw[0]
        self.late6 = raw[2][2]
        self.lnge6 = raw[2][3]
        self.img = raw[2][7]
        self.name = raw[2][8]

        self.portal = {
            'pguid': self.pguid,
            'late6': self.late6,
            'lnge6': self.lnge6,
            'img': self.img,
            'name': self.name,
            'tile': tile
        }


class IITCModel:
    """For update from iitc"""
    def __init__(self, data):
        self.data = data['data']

        teams = {
            'E': 1,
            'R': 2,
            'N': 3
        }

        self.img = self.data.get('image')
        self.name = self.data.get('title')
        self.team = teams.get(self.data.get('team'))
        if not self.team:
            self.team = self.data.get('team')

        self.late6 = self.data.get('latE6')
        self.lnge6 = self.data.get('lngE6')

        self.guid = data.get('guid')

        if not self.guid:
            self.guid = self.data.get('guid')

        self.data = {'data': {
                'image': self.img,
                'title': self.name,
                'latE6': self.late6,
                'lngE6': self.lnge6,
                'team': self.team,
                'guid': self.guid
            }
        }
        
        self.iitc_achive = {
            'img': self.img,
            'name': self.name,
            'late6': self.late6,
            'lnge6': self.lnge6,
            'pguid': self.guid,
            'team': self.team,
        }

        self.update = {
            'img': self.img,
            'name': self.name,
            'late6': self.late6,
            'lnge6': self.lnge6,
            'pguid': self.guid
        }


class IITCRbotModel(object):
    "For iitc plugin"
    def __init__(self, data):
        self.name = data['name']
        self.latE6 = data['late6']
        self.lngE6 = data['lnge6']
        self.timestamp = data['timestamp']
        self.owner = data['player']
        self.guid = None
        try:
            self.guid = data['pguid']
        except:
            pass

        self.data = {
                "type": "Feature",
                "properties": {
                  "name": self.name,
                  "popupContent": self.name + "<br />Player: " + self.owner,
                  "timestamp": round(self.timestamp/1000),
                  "guid": self.guid
                },
                "geometry": {
                  "type": "Point",
                  "coordinates": [
                    self.lngE6/1E6,
                    self.latE6/1E6
                  ]
                }
              }


class ProfileScannerModel(object):
    def __init__(self, query):
        teams = {
            'ALIENS': 1,
            'RESISTANCE': 2
        }

        self.player = query['playername']
        self.lvl = query['verifiedLevel']
        self.team = teams[query['team']]
        self.badges = self.get_list_badges(query['highlightedAchievements'])
        self.metrics = query['metrics']
        self.ap = query['ap']
        self.gplus = query.get('gPlusId')
        self.missions = query['highlightedMissionBadges']
        self.update = int(round(time.time() * 1000))

        for i in self.badges:
            if i.get('title') == 'Guardian':
                self.guardian = i['graduate']
                break
            else:
                self.guardian = 0

        self.profile = {
            'playername': self.player,
            'lvl': self.lvl,
            'team': self.team,
            'badges': self.badges,
            'metrics': self.metrics,
            'ap': self.ap,
            'mission_badges': self.missions,
            'update': self.update,
            'guardian': self.guardian,
            'gplus': self.gplus
        }

    def get_last_medal(self, medal_list):
        value = None
        count = 0
        badgeImageUrl = None
        for i in medal_list:
            if not i['locked']:
                count += 1
                value = i['value']
                badgeImageUrl = i['badgeImageUrl']
        return [count, value, badgeImageUrl]

    def get_list_badges(self, result):
        medals = []
        for i in result:
            if len(i['tiers']) == 1:
                medals.append({'title': i['title'], 'timestampAwarded': i['timestampAwarded'],
                               'badgeImageUrl': i['tiers'][0]['badgeImageUrl'], 'description': i['description']})
            elif i['timestampAwarded'] == "-1":
                continue
            else:
                parsed = self.get_last_medal(i['tiers'])
                medals.append({'title': i['title'], 'timestampAwarded': i['timestampAwarded'], 'graduate': parsed[0],
                               'value': parsed[1], 'badgeImageUrl': parsed[2], 'description': i['description']})
        return medals


class InventoryModel(object):
    def __init__(self, data):
        self.item_id = data[0]
        self.timestamp = int(round(time.time() * 1000))
        self.description = data[2]
        self.agent_id = self.description.get('inInventory').get('playerId')

        self.data = {
            'item_id': self.item_id,
            'agent_id': self.agent_id,
            'description': json.dumps(self.description),
            'timestamp': self.timestamp
        }