"""Get log from ingress.com"""
import sys

sys.path.append('./')

from bot.parser import TilesParser
from db.postgredb import AchieveLog
import multiprocessing
import time
from db.redisdb import RedisCookiesModule, RedisSettingsModule, TilesLogModule
from bot import bot, util
import logging

from bot.util import deg2num_to_ingress


def streamer(tiles):

    cookies = RedisCookiesModule().get_cookie()
    if cookies:
        intel = bot.Intel(cookies)

        tile_bot_list = []

        for i in tiles:
            tile_bot_list.append(i)
            if len(tile_bot_list) == 1:
                result = {}
                try:
                    result = intel.fetch_map(tile_bot_list)
                except:
                    print('Time out')
                    pass
                if result.get('result'):
                    TilesParser(result).get_portals()
                tile_bot_list = []

                if result.get('error') == 'out of date':
                    RedisSettingsModule.version_control_del()
                    logging.error('get_log: {}'.format(result['error']))
                elif result.get('error') == 'cookies':
                    util.error_cookies(cookies)
                    logging.error('get_log: {} error'.format(result['error']))

    else:
        logging.error('get_log: Cookies not found')
        RedisCookiesModule().load_cookies()


def create_stream(tiles, count):
    ps = multiprocessing.Process(target=streamer, args=(tiles,), name='stream_{}'.format(count))
    jobs.append(ps)
    ps.start()

    logging.error('Streamer stram_{} started'.format(count))


if __name__ == '__main__':
    logging.basicConfig(filename='error_log', level=logging.ERROR, format='%(asctime)s %(message)s')
    RedisCookiesModule().load_cookies()
    jobs = []

    count_name = 0
    portals = []
 #   portals = AchieveLog().get_no_pguid_portals()
    count_temp = 0

    print('Portals with no guid', len(portals))

    tiles_list = []
    for i in portals:
        lat = i.get('late6')
        lng = i.get('lnge6')

        if not lat and lng:
            continue

        xtile, ytile = deg2num_to_ingress(lat, lng)
        tile_size = 1
        maxx = xtile + tile_size
        maxy = ytile + tile_size

        minx = xtile - tile_size
        miny = ytile - tile_size

        while minx < maxx:
            while miny < maxy:
                result = '15_'+str(minx)+'_'+str(miny)+'_0_8_100'
                if result not in tiles_list:
                    tiles_list.append(result)
                miny += 1
            minx += 1
            miny = ytile - tile_size

        count_name += 1
#        create_stream(tiles_list, count_name)
        count_temp += 1
        tiles_list = []
        if count_temp > 20:
            time.sleep(30)
            count_temp = 0

    while True:
        for j in jobs:
            if not j.is_alive():
                jobs.remove(j)
        time.sleep(2)

        if len(jobs) == 0:
            values = TilesLogModule().get_query()
            if values:
                TilesParser({'none': 'none'}).from_redis_to_psql(values)
            else:
                break
