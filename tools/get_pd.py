"""Get portal details"""
import sys


sys.path.append('./')

from bot.util import TimeCl
import multiprocessing
import time
from db.redisdb import RedisTaksModule, RedisCookiesModule, RedisLogModule, RedisSettingsModule
from bot import bot
from bot.parser import PortalParser
from db.postgredb import PortalDetail
import settings
import logging


def expired(timestamp):
    if TimeCl(timestamp).daydiff() > 2:
        return True


def worker(task):
    """thread worker function"""
    counter = 0
    cookies = None

    if counter == 0:
        cookies = RedisCookiesModule().get_cookie()
    counter += 1
    if cookies:
        portal_list = PortalDetail().get_pd_list(task['task'])
        if not portal_list:
            time.sleep(50)
            return

        for portaldb in portal_list:
            intel = bot.Intel(cookies)
            result = intel.fetch_portal(portaldb['guid'])
            if result.get('result'):
                PortalParser(portaldb, result['result'])

            if portaldb['expired'] > 0 and expired(portaldb['expired']):
                PortalDetail().delete_portal(portaldb['guid'])
            time.sleep(5)
        if counter == 4:
            counter = 0

    time.sleep(settings.INSPECTOR_SLEEP)
    RedisTaksModule().load_tasks()
    RedisCookiesModule().load_cookies()


def create_worker(task):
    """Create worker"""
    p = multiprocessing.Process(target=worker, args=(task,), name='pd_{}'.format(task['task']))
    jobs.append(p)
    p.start()
    logging.info('Worker {} started'.format(task['task']))

if __name__ == '__main__':
    logging.basicConfig(filename='error_log', level=logging.ERROR, format='%(asctime)s %(message)s')
    RedisTaksModule().load_tasks()
    RedisCookiesModule().load_cookies()
    jobs = []
    tasks = RedisTaksModule().get_tasks('pd', all=True)

    for task in tasks:
        create_worker(task)
        time.sleep(1)
    time.sleep(2)

    while True:
        for j in jobs:
            if not j.is_alive():
                jobs.remove(j)
                create_worker(RedisTaksModule().get_tasks(j.name))
        time.sleep(2)

