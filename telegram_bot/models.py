from datetime import datetime

from bot.util import portal_url


class TelPortalDetailModel(object):
    def __init__(self, diff, portaldb, portal_from_intel):
        self.diff = diff
        self.portaldb = portaldb
        self.portal_from_intel = portal_from_intel

    def sofa(self, get_one=False):
        jdata = self.portal_from_intel

        if type(jdata) is not list and jdata.get('error'):
            return jdata.get('error')

        def mods(query):
            a = ''
            if query:
                for i in query['mods']:
                    if i:
                        a += '        {}({}) by <b>{}</b>\n'.format(i[1], i[2], i[0])
            return a

        def resonators(query):
            a = ''
            if query:
                for owner, lvl in query['resonators']:
                    a += '        L{}  by <b>{}</b>\n'.format(lvl, owner)
            return a

        team = {
            1: 'E',
            2: 'R',
            3: 'N'
        }
        if jdata:
            portals = ''
            if get_one:
                portals += '<pre>{}{}</pre> Portal: <b>{}</b>, Owner: {}\n' \
                           '{}\n' \
                           '<code>Mods:</code>\n{}' \
                           '<code>Resonators:</code>\n{}' \
                           '\n<code>Last changes:</code>\n{}'.format(team[jdata['team']], jdata['lvl'], jdata['name'], jdata.get('player'),
                           datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                           mods(jdata), resonators(jdata), self.parse_diff(verbose=False))
                return portals

            for portal in jdata:
                portals += '<pre>{}{}</pre> Portal: <b>{}</b>, Owner: {}\n' \
                           '{}\n' \
                           '<code>Mods:</code>\n{}' \
                           '<code>Resonators:</code>\n{}' \
                           '\n'.format(team[portal['team']], portal['lvl'], portal['name'], portal.get('player'),
                           datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                           mods(portal), resonators(portal))
            return portals

        return 'Unknown Error!'


    def parse_diff(self, verbose=True):
        teams = {
            1: 'E',
            2: 'R',
            3: 'N'
        }
        keys = self.diff.keys()
        a = ''
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if 'player' in keys:
            if self.diff['player'] == '':
                a += '<b>Portal now Neutral</b>'
            else:
                a += 'Owner now <b>{}</b>({})\n'.format(self.diff['player'], teams[self.diff['team']])

        if 'mods' in keys:
            mods = self.diff['mods']

            if mods[0] and len(mods[0]) != 3:
                a += '   <b>{}</b>({}) deployed mod {} ({})\n'.format(mods[0], teams[self.diff['team']], mods[1], mods[2])
            else:
                for i in mods:
                    if i:
                        a += '   <b>{}</b>({}) deployed mod {} ({})\n'.format(i[0], teams[self.diff['team']], i[1], i[2])
        if 'resonators' in keys:
            res = self.diff['resonators']
            if len(list(res)) > 2:
                for z in res:
                    if z:
                        a += '    <b>{}</b>({}) deployed resonator L{}\n'.format(z[0], teams[self.diff['team']], z[1])
            else:
                a += '    <b>{}</b>({}) deployed resonator L{}\n'.format(res[0], teams[self.diff['team']], res[1])

        if verbose:
            portal_diff_verbose = '<b>{}</b>\n{}\n{} {}\n{}\n'.format(self.portaldb['name'], self.portaldb['address'],
                                                                      a, timestamp, portal_url(self.portaldb))
            return portal_diff_verbose

        portal_diff = '{}'.format(a)

        return portal_diff


class TelegramMessageModel(object):
    def __init__(self, data):
        self.message = data.message
        self.chat_id = self.message.chat.id
        self.text = self.message.text
        print(self.text)

    def action(self):
        default = None

        if 'ingress.com/intel' in self.text:
            return 'monitor'

        try:
            return self.text.split()[0].lower()
        except IndexError:
            return default

    def argument(self):
        default = None
        if 'ingress.com/intel' in self.text:
            return self.text.split()[0]

        try:
            return self.text.split()[1]
        except IndexError:
            return default


def player_profile(data):
    data = data['result']['profile']
    import bot.util as util
    teams = {
        1: 'ENL',
        2: 'RES'
    }
    badges = {
        1: 'BRONZE',
        2: 'SILVER',
        3: 'GOLD',
        4: 'PLATINUM',
        5: 'BLACK'
    }

    if data:
        profile = 'Profile of {} <b>{}</b>\n'.format(data['playername'], teams[data['team']])
        profile += 'Lvl: <b>{}</b> AP: <b>{}</b>\n'.format(data['lvl'], data['ap'])
        if data['badges']:
            for i in data['badges']:
                if i.get('graduate'):
                    profile += '<b>{}</b> {} got {}\n'.format(i['title'], badges[i['graduate']],
                                                              util.TimeCl(int(i['timestampAwarded'])).humans())
                    continue
                profile += '<b>{}</b> got {}\n'.format(i['title'], util.TimeCl(int(i['timestampAwarded'])).humans())

        return profile


def guards(jdata):
    import bot.util as util
    jdata = jdata.get('result')
    if jdata:
        player = jdata.get('args').get('player')
        jdata = jdata.get('achievements')
        portals = ''
        if not jdata:
            portals += 'agent not found!'
        else:
            for portal in jdata:
                portals += '<b>{}</b>, <a href="{}">{}</a>({})\n' \
                           ''.format(util.TimeCl(portal['timestamp']).daydiff(),
                                     portal_url(portal), portal.get('name'),
                                     portal.get('address'))
            if player:
                portals += '<a href="https://ingress-guard.tk/#/player/{}">Show on ingress-guard</a>\n'.format(player)
        return portals


def history(jdata):
    import bot.util as util
    plains = {
        1: ' deployed a Resonator on ',
        2: ' captured ',
        3: ' destroyed a Resonator on ',
        4: ' linked ',
        5: ' created a Control Field @',
        6: ' destroyed the Link ',
        7: ' destroyed a Control Field @',
        8: ' deployed a Portal Fracker on ',
        9: ' deployed a Beacon on ',
    }

    if jdata:
        jdata = jdata['result']['actions']
        counter = 0
        portals = 'Comm log\n'
        for portal in jdata:
            counter += 1
            portals += '{} {} <a href="{}">{}</a> {}\n' \
                       ''.format(datetime.fromtimestamp(int(portal['timestamp']/1000)).strftime('%Y-%m-%d %H:%M:%S'),
                                 plains[portal['plain']], portal_url(portal), portal['name'],
                                 util.address_convertor(portal.get('address')))
            if counter > 40:
                break

        return portals
    return {'error': 'history not found'}


def portal_history(jdata):
    import bot.util as util
    plains = {
        1: ' deployed a Resonator on ',
        2: ' captured ',
        3: ' destroyed a Resonator on ',
        4: ' linked ',
        5: ' created a Control Field @',
        6: ' destroyed the Link ',
        7: ' destroyed a Control Field @',
        8: ' deployed a Portal Fracker on ',
        9: ' deployed a Beacon on ',
    }

    if jdata:
        jdata = jdata['result']['portal_history']['history']
        counter = 0
        portals = 'Comm log\n'
        for portal in jdata:
            counter += 1
            portals += '{} {} <a href="{}">{}</a> {}\n' \
                       ''.format(datetime.fromtimestamp(int(portal['timestamp']/1000)).strftime('%Y-%m-%d %H:%M:%S'),
                                 plains[portal['plain']], portal_url(portal), portal['name'],
                                 util.address_convertor(portal.get('address')))
            if counter > 40:
                break

        return portals
    return {'error': 'history not found'}


def user_from(jdata):
    if jdata:
        jdata = jdata['result']['player_from']
        user = 'Agent <b>{}</b> from <b>{}</b>. Last update {}\n' \
               ''.format(jdata['player'], jdata['live_in'],
                         datetime.fromtimestamp(int(jdata['update']/1000)).strftime('%Y-%m-%d %H:%M:%S'))
        return user

    return {'error': 'User not found in base!'}


def search_player(jdata):
    teams = {
        1: 'ENL',
        2: 'RES'
    }
    if jdata:
        jdata = jdata['result']['players']
        users = 'Users like: \n'
        for user in jdata:
            users += '    {} - {} ({})\n'.format(user['player'], user['player'].lower(), teams[user['team']])
        return users
    return {'error': 'User not found!'}


def monitor_add(jdata):
    if jdata:
        jdata = jdata['result']['monitor']

        monitor = 'Portal {} added, expired in 2 days\n address {}\n'.format(jdata.get('name'), jdata.get('address'))

        return monitor

    return {'error': 'can`t add'}
