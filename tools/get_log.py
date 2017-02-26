"""Get log from ingress.com"""
import sys


sys.path.append('./')

from bot.parser import CommPreParser
import multiprocessing
import time
from db.redisdb import RedisTaksModule, RedisCookiesModule, RedisSettingsModule
from bot import bot
import settings
import logging
from bot import util


def worker(task):
    """thread worker function"""
    mints = -1
    counter = 0

    while True:

        if counter == 0:
            cookies = RedisCookiesModule().get_cookie()
        counter += 1
        tnum = 1
        if cookies:
            tnum = settings.COM_SLEEP

            intel = bot.Intel(cookies, task)

            # try get data from intel
            result = intel.fetch_msg(mints)

            if result.get('error') == 'out of date':
                RedisSettingsModule.version_control_del()
                logging.error('get_log: {}'.format(result['error']))
            elif result.get('error') == 'cookies':
                util.error_cookies(cookies)
                counter = 0
                logging.error('get_log: {} error'.format(result['error']))

            if result.get('result'):
                mints = result['result'][0][1] + 1
                CommPreParser(result)
            else:
                tnum = 0.4
        else:
            logging.error('get_log: Cookies not found')
            RedisCookiesModule().load_cookies()

        if counter == 20:
            counter = 0

        time.sleep(tnum)


def create_worker(task):
    """Create worker"""
    p = multiprocessing.Process(target=worker, args=(task,), name='comm_{}'.format(task['id']))
    jobs.append(p)
    p.start()
    logging.info('Worker {} started'.format(task['id']))

if __name__ == '__main__':
    logging.basicConfig(filename='error_log', level=logging.ERROR, format='%(asctime)s %(message)s')
    RedisTaksModule().load_tasks()
    RedisCookiesModule().load_cookies()
    jobs = []
    tasks = RedisTaksModule().get_tasks('comm', all=True)
    for task in tasks:
        create_worker(task)
    time.sleep(2)

    while True:
        for j in jobs:
            if not j.is_alive():
                jobs.remove(j)
                print(j.name)
                create_worker(RedisTaksModule().get_tasks(j.name))
                RedisCookiesModule().load_cookies()
        time.sleep(2)