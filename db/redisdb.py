import os
import redis
from db.postgredb import *


class RedisTaksModule:
    """
        DB 0 - tasks
        DB 1 - cookies
        DB 2 - log
        DB 3 - settings
        DB 4 - iitc log
        DB 5 - fake log
        DB 6 - tiles log
        DB 7 - Players
    """
    current_milli_time = int(round(time.time() * 1000))
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

    @classmethod
    def load_tasks(cls):
        tasks = PTasks().get_comm_task()
        pipe = cls.r.pipeline()
        for task in tasks:
            pipe.set('comm_{}'.format(task['id']), json.dumps(task))

        pd_tasks = PTasks().get_pd_task()
        for task in pd_tasks:
            pipe.set('pd_{}'.format(task['task']), json.dumps(task))
        pipe.execute()

    @classmethod
    def get_tasks(cls, same, all=False):
        if all:
            keys = cls.r.keys('{}_*'.format(same))
            values_list = []
            for i in keys:
                values_list.append(json.loads(cls.r.get(i).decode('UTF-8')))
            return values_list
        return json.loads(cls.r.get(same).decode('UTF-8'))


class RedisCookiesModule(RedisTaksModule):
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)

    @classmethod
    def load_cookies(cls):
        cookies = PCookies().loadCookie()
        pipe = cls.r.pipeline()
        for cookie in cookies:
            if cookie['status'] == 'ok':
                pipe.set(cookie['id'], json.dumps(cookie))
            else:
                pipe.delete(cookie['id'])
        pipe.execute()

    @classmethod
    def get_cookie(cls):
        keys = cls.r.keys('*')
        values_list = []
        for i in keys:
            cookie = json.loads(cls.r.get(i).decode('UTF-8'))
            if cookie['status'] == 'ok':
                values_list.append(cookie)
        if values_list:
            return values_list[round(random.uniform(0, len(values_list) - 1))]

    @classmethod
    def get_scanner_cookie(cls):
        keys = cls.r.keys('*')
        values_list = []
        for i in keys:
            cookie = json.loads(cls.r.get(i).decode('UTF-8'))
            if cookie['status'] == 'ok' and cookie.get('scanner_cookie'):
                values_list.append(cookie)
        if values_list:
            return values_list[int(random.uniform(0, len(values_list) - 1))]

    @classmethod
    def error_cookie(cls, id):
        cls.r.delete(id)


class RedisLogModule(RedisTaksModule):
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=2)

    @classmethod
    def log_achive_query(cls, query):
        pipe = cls.r.pipeline()
        for i in query:
            pipe.set('{}_{}'.format(i['timestamp'], i['late6']), json.dumps(i))
        pipe.execute()

    @classmethod
    def get_query(cls, limit=100):
        all_keys_list = cls.r.keys('*')

        if len(all_keys_list) > limit:
            log_id_list = sorted(all_keys_list)[:limit]
            pipe = cls.r.pipeline()
            for query in log_id_list:
                pipe.get(query)
            values = pipe.execute()
            pipe = cls.r.pipeline()
            for query in log_id_list:
                pipe.delete(query)
            pipe.execute()

            return values


class RedisActionsLogModule(RedisTaksModule):
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=5)

    @classmethod
    def log_actions_query(cls, query):
        pipe = cls.r.pipeline()
        for i in query:
            pipe.set('{}_{}'.format(i['timestamp'], i['mguid']), json.dumps(i))
        pipe.execute()

    @classmethod
    def get_query(cls, limit=100):
        all_keys_list = cls.r.keys('*')

        if len(all_keys_list) > limit:
            log_id_list = sorted(all_keys_list)[:limit]
            pipe = cls.r.pipeline()
            for query in log_id_list:
                pipe.get(query)
            values = pipe.execute()
            pipe = cls.r.pipeline()
            for query in log_id_list:
                pipe.delete(query)
            pipe.execute()

            return values


class RedisSettingsModule(RedisTaksModule):
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=3)

    @classmethod
    def version_control_set(cls, version):
        cls.r.set('version', version)

    @classmethod
    def version_control_get(cls):
        version = cls.r.get('version')
        if version:
            return version.decode('UTF-8')

    @classmethod
    def version_control_del(cls):
        cls.r.delete('version')


class IITCLogModule():
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=4)

    @classmethod
    def log_query(cls, query):
        cls.r.set('{}'.format(query['data']['guid']), json.dumps(query))

    @classmethod
    def get_query(cls):
        all_keys_list = cls.r.keys('*')
        log_id_list = []

        if len(all_keys_list) > 50:
            log_id_list = sorted(all_keys_list)[:50]
        elif len(all_keys_list) > 20:
            log_id_list = sorted(all_keys_list)[:20]
        elif len(all_keys_list) < 20:
            log_id_list = sorted(all_keys_list)[:1]

        if log_id_list:
            pipe = cls.r.pipeline()
            for query in log_id_list:
                pipe.get(query)
            values = pipe.execute()
            pipe = cls.r.pipeline()
            for query in log_id_list:
                pipe.delete(query)
            pipe.execute()

            return values


class TilesLogModule():
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=6)

    @classmethod
    def log_query(cls, query):
        pipe = cls.r.pipeline()
        for i in query:
            pipe.set('{}{}'.format(i['late6'], i['lnge6']), json.dumps(i))
        pipe.execute()

    @classmethod
    def get_query(cls):
        all_keys_list = cls.r.keys('*')
        log_id_list = []

        if len(all_keys_list) > 0:
            log_id_list = sorted(all_keys_list)[:50]

        if log_id_list:
            pipe = cls.r.pipeline()
            for query in log_id_list:
                pipe.get(query)
            values = pipe.execute()
            pipe = cls.r.pipeline()
            for query in log_id_list:
                pipe.delete(query)
            pipe.execute()

            return values


class PlayerLogModule():
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=7)

    @classmethod
    def log_query(cls, query):
        pipe = cls.r.pipeline()
        for i in query:
            i.update({'player_lowercase': i['player'].lower()})
            pipe.set('{}'.format(i['player_lowercase']), json.dumps(i))
        pipe.execute()

    @classmethod
    def get_query(cls):
        all_keys_list = cls.r.keys('*')

        pipe = cls.r.pipeline()
        for query in all_keys_list:
            pipe.get(query)
        values = pipe.execute()
        pipe = cls.r.pipeline()
        for query in all_keys_list:
            pipe.delete(query)
        pipe.execute()

        return values

class PortalsLogModule():
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=8)

    @classmethod
    def log_query(cls, query):
        pipe = cls.r.pipeline()
        for i in query:
            pipe.set('{}_{}'.format(i['late6'], i['lnge6']), json.dumps(i))
        pipe.execute()

    @classmethod
    def get_query(cls):
        all_keys_list = cls.r.keys('*')

        pipe = cls.r.pipeline()
        for query in all_keys_list:
            pipe.get(query)
        values = pipe.execute()
        pipe = cls.r.pipeline()

        return values


class RedisIpCheck:
    current_milli_time = int(round(time.time() * 1000))
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=9)

    @classmethod
    def check_ip(cls, ip):
        query = cls.r.get('s_{}'.format(ip))

        if not query:
            cls.r.set('s_{}'.format(ip), 1, 5)
        cls.r.incr('s_{}'.format(ip), 1)
        try:
            tryes = int(query.decode('UTF-8'))
            if tryes > 20:
                cls.r.expire('s_{}'.format(ip), 60)
                return True
        except:
            pass

    @classmethod
    def get_ad_stat(cls, ip):
        ad_query = cls.r.get(ip)
        if ad_query:
            ad_status = int(ad_query.decode('UTF-8'))
            if ad_status > 4:
                return True


class RedisSubscription:
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=10)
    @classmethod
    def pub_log(self, log):
        self.r.publish('logs', log)