import json
import os
import time
import subprocess
from datetime import datetime
import uuid

import math
from math import pi, sin, cos, tan, asin, radians, sqrt, log

from db import redisdb
from db import postgredb
from db.postgredb import PlayerPg, PortalDetail, ActionsLog


class UserStatistics():
    def get_list_users(self):
        result = PlayerPg().get_all_users_to_list()
        return result

    def get_where_live(self, late6, lnge6):
        query = PortalDetail().find_address_by_geo(late6, lnge6)[0]
        address = address_convertor(query['address'])
        return address

    def create_statistics(self, player):
        query = ActionsLog().find_player_actions_full(player)
        if not query:
            return
        result = self.filter_list(query)

        late6 = None
        lnge6 = None
        live_in = None

        if result:
            late6 = result[0]
            lnge6 = result[1]
            live_in = self.get_where_live(late6, lnge6)

        data = {
            'player': player,
            'late6': late6,
            'lnge6': lnge6,
            'live_in': live_in
        }

        PlayerPg().create_player_statistics(data)
        return data

    def sort_list(self, query):
        main_list = []
        second_list = []
        late6 = None
        lnge6 = None
        for i in query:
            if not late6:
                late6 = i[0]
                lnge6 = i[1]

            if math.fabs(i[0] - late6) < 1000000 and math.fabs(i[1] - lnge6) < 1000000:
                main_list.append((i[0], i[1]))
            else:
                second_list.append((i[0], i[1]))

        return main_list, second_list

    def central_point(self, point_list):
        lat = 0
        lng = 0
        for l, g in point_list:
            lat += l
            lng += g

        cplat = round(lat / len(point_list))
        cplng = round(lng / len(point_list))
        return cplat, cplng

    def filter_list(self, query):
        ml = None
        sl = None
        count = None
        for i in range(10):
            if count == None:
                ml, sl = self.sort_list(query)
                count = 1
                continue
            if len(ml) < len(sl):
                ml, sl = self.sort_list(sl)
            else:
                return self.central_point(ml)

        return {'error': 'player is bomj'}


class TimeCl(object):

    def __init__(self, timestamp=1):
        self.timestamp = timestamp
        self.seconds, self.millis = divmod(timestamp, 1000)
        self.tsnow = datetime.now()
        self.timediff = self.tsnow - datetime.fromtimestamp(self.seconds)
        """
            Current time in secs
        """
        self.current_sec = int(round(time.time()))

    """
        Return now - days in timestamp
    """
    def past_from_days(self, days):
        return (self.current_sec - days * 86400) * 1000

    def daydiff(self):
        return self.timediff.days

    def secdiff(self):
        return self.timediff.seconds

    def mindiff(self):
        return round(self.timediff.seconds / 60)

    def humans(self):
        return datetime.fromtimestamp(int(self.timestamp/1000)).strftime('%Y-%m-%d %H:%M:%S')


def area_max_min_latlng(late6, lnge6):
    area = {
        'maxlat': int(int(late6) + 2 * 1E6),
        'minlat': int(int(late6) - 2 * 1E6),
        'maxlng': int(int(lnge6) + 4 * 1E6),
        'minlng': int(int(lnge6) - 4 * 1E6),
    }
    return area


def error_cookies(cookie):
    id = cookie['id']
    postgredb.PCookies().errorCookie(id)
    redisdb.RedisCookiesModule().error_cookie(id)


def zoom_area(zoom):
    if zoom == 9:
        multiplier = 0.5
    elif zoom == 10:
        multiplier = 0.3
    elif zoom == 11:
        multiplier = 0.15
    elif zoom == 12:
        multiplier = 0.06
    else:
        multiplier = 0.03

    return multiplier*1E6


def token():
    return str(uuid.uuid4())[:20]


def ada_execute(my_dicts):
    copies = []
    for n in range(len(my_dicts)):

        check = my_dicts.pop()

        if check in my_dicts and check not in copies:
            copies.append(check)
        else:
            my_dicts.append(check)
    if copies:
        return copies


def portal_url(portal):
    lat = portal['late6']/1000000
    lng = portal['lnge6']/1000000
    return 'https://www.ingress.com/intel?ll='+str(lat)+','+str(lng)+'&z=17&pll='+str(lat)+','+str(lng)


def portal_url_latlng(late6, lnge6):
    lat = late6/1000000
    lng = lnge6/1000000
    return 'https://www.ingress.com/intel?ll='+str(lat)+','+str(lng)+'&z=17&pll='+str(lat)+','+str(lng)


def daemon_statistic():
    process = subprocess.Popen("ps aux | grep python | grep -v grep", shell=True, stdout=subprocess.PIPE,)
    process_list = []
    for line in process.stdout:
        process_list.append(line.decode('UTF-8'))
    return process_list


def address_convertor(address):
    try:
        if address:
            addr = address.split(',')
            if len(addr) == 5:
                return '{}, {}'.format(addr[2], addr[3])
            elif len(addr) == 1:
                return '{}'.format(addr[0])
            elif len(addr) == 6:
                return '{}, {}, {}'.format(addr[2], addr[3], addr[4])
            else:
                return '{}, {}'.format(addr[1], addr[2])
    except:
        return address


def calc_tile(lng, lat, zoomlevel):
    tilecounts = [1,1,1,40,40,80,80,320,1E3,2E3,2E3,4E3,8E3,16E3,16E3,32E3]
    rlat = radians(lat)
    tilecount = tilecounts[zoomlevel]
    xtile = int((lng + 180.0) / 360.0 * tilecount)
    ytile = int((1.0 - log(tan(rlat) + (1 / cos(rlat))) / pi) / 2.0 * tilecount)
    return xtile, ytile


def calc_dist(lat1, lng1, lat2, lng2):
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = lat1 - lat2
    dlng = lng1 - lng2
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2* asin(sqrt(a))
    m = 6367.0 * c * 1000
    return m


def point_in_poly(x, y, poly):
    n = len(poly)
    inside = False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside


def transform(wgLat, wgLon):
    """
    transform(latitude,longitude) , WGS84
    return (latitude,longitude) , GCJ02
    """
    a = 6378245.0
    ee = 0.00669342162296594323
    if (outOfChina(wgLat, wgLon)):
        mgLat = wgLat
        mgLon = wgLon
        return mgLat,mgLon
    dLat = transformLat(wgLon - 105.0, wgLat - 35.0)
    dLon = transformLon(wgLon - 105.0, wgLat - 35.0)
    radLat = wgLat / 180.0 * pi
    magic = sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
    dLon = (dLon * 180.0) / (a / sqrtMagic * cos(radLat) * pi)
    mgLat = wgLat + dLat
    mgLon = wgLon + dLon
    return mgLat,mgLon


def outOfChina(lat, lon):
    if (lon < 72.004 or lon > 137.8347):
        return True
    if (lat < 0.8293 or lat > 55.8271):
        return True
    return False


def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(y * pi) + 40.0 * sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * sin(y / 12.0 * pi) + 320 * sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformLon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(x * pi) + 40.0 * sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * sin(x / 12.0 * pi) + 300.0 * sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret


def deg2num_to_ingress(latE6, lngE6):
    latE6 = latE6/1E6
    lngE6 = lngE6/1E6
    zoom = 15
    l, t = transform(lngE6, latE6)
    xtile, ytile = calc_tile(l, t, zoom)
    result = '17_'+str(xtile)+'_'+str(ytile)+'_0_8_100'
    return xtile, ytile