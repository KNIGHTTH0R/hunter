import json
import random
import uuid

import psycopg2
import time
from psycopg2.extras import RealDictCursor
import settings


class PostgreLocal:
    def execute_query(self, query, args_query=None, test=False, returning=False):
        if query.startswith('SELECT'):
            self.pgdb = psycopg2.connect(settings.PSQL_SECONDARY)
        else:
            self.pgdb = psycopg2.connect(settings.PSQL_PRIMARY)

        cur = self.pgdb.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if test:
            print(query, args_query)
            print(cur.mogrify(query, args_query))

        try:
            if args_query:
                cur.execute(query, args_query)
            else:
                cur.execute(query)

            if query.startswith('SELECT') or returning:
                result = [dict((cur.description[i][0], value)
                          for i, value in enumerate(row)) for row in cur.fetchall()]
                self.pgdb.commit()
                return result

        except Exception as e:
            self.pgdb.rollback()
            raise e
        else:
            self.pgdb.commit()

    def mogrify_query(self, query, args_query=None):
        cur = self.pgdb.cursor(cursor_factory=psycopg2.extras.DictCursor)
        result = None
        if args_query:
            result = cur.mogrify(query, args_query)
        return result


class PTasks(PostgreLocal):
    """Tasks module"""

    def get_comm_task(self):
        if settings.SERVER_NAME == 'all':
            comm_task = self.execute_query("SELECT * FROM tasks;", )
            return comm_task
        comm_task = self.execute_query("SELECT * FROM tasks WHERE server = %s;",
                                       (settings.SERVER_NAME, ), )
        return comm_task

    def get_pd_task(self):
        return self.execute_query("SELECT DISTINCT ON (task) task FROM inspector;", )


class PCookies(PostgreLocal):
    """Cookies module"""
    def loadCookie(self):
        return self.execute_query("SELECT id, cookie, status FROM cookies;", )

    def get_crft(self):
        query = self.execute_query("SELECT cookie, email FROM cookies WHERE status = 'ok';", )
        if not query:
            return None, None
        result = query[round(random.uniform(0, len(query) - 1))]

        if result:
            if result['cookie'] != '' and result['cookie']:
                return result['cookie'], result['email']
            else:
                self.update_cookie_status(result['email'], 'error')
                return None, None
        else:
            print('Not found cookies with status free')
            return None, None

    def errorCookie(self, id):
        self.execute_query("UPDATE cookies SET status = 'error' WHERE id = %s;", (id, ))

    def get_scanner_cookies(self):
        return self.execute_query("SELECT * FROM cookies WHERE tag = 'scanner';")

    def get_user_scanner_cookies(self, user):
        return self.execute_query("SELECT * FROM scanner_player_id WHERE email = %s AND cookie IS NOT NULL;", (user, ), )

    def insert_scanner_cookie(self, cookie, email):
        self.execute_query("UPDATE cookies SET scanner_cookie = %s, slastupdate = %s WHERE email = %s;",
                           (cookie, int(round(time.time() * 1000)), email))


class ActionsLog(PostgreLocal):
    def insert_comm(self, keys_list, values_list):
        """INSERT ACTIONS LIST"""
        if not values_list:
            return
        comm_list_template = ','.join(['%s'] * len(values_list))
        insert_actions_query = 'INSERT INTO actions {0} VALUES {1} ON CONFLICT (mguid) DO NOTHING;' \
                               ''.format(keys_list, comm_list_template)
        self.execute_query(insert_actions_query, values_list)

    def insert_player(self, keys_list, values_list):
        """INSERT PLAYERS LIST"""
        if not values_list:
            return
        player_list_template = ','.join(['%s'] * len(values_list))
        insert_players_query = 'INSERT INTO player {0} VALUES {1} ON CONFLICT ON CONSTRAINT player_player_idx DO ' \
                               'UPDATE SET player = EXCLUDED.player, late6 = EXCLUDED.late6, lnge6 = EXCLUDED.lnge6, ' \
                               'address = EXCLUDED.address, team = EXCLUDED.team, plain = EXCLUDED.plain, name = EXCLUDED.name, ' \
                               'timestamp = EXCLUDED.timestamp;' \
                               ''.format(keys_list, player_list_template)
        self.execute_query(insert_players_query, values_list)

    def find_player_actions(self, player, lim=1000):
        return self.execute_query("SELECT * FROM actions WHERE lower(player) = %s ORDER BY timestamp desc LIMIT %s;",
                                  (player.lower(), lim, ), )

    def find_player_actions_full(self, player):
        result = self.execute_query("SELECT late6, lnge6 FROM actions WHERE player = %s;",
                                    (player, ))
        return result


class AchieveLog(PostgreLocal):
    def insert_achive(self, keys_list, values_list):
        """INSERT ACHIVE LIST"""
        if not values_list:
            return
        achieve_list_template = ','.join(['%s'] * len(values_list))
        insert_ach_query = 'INSERT INTO achive {0} VALUES {1} ' \
                           'ON CONFLICT ON CONSTRAINT achive_late6_lnge6_key DO UPDATE SET player = EXCLUDED.player,' \
                           ' team = EXCLUDED.team, timestamp = EXCLUDED.timestamp, ' \
                           'name = EXCLUDED.name, address = EXCLUDED.address, status = EXCLUDED.status, ' \
                           'ada = EXCLUDED.ada, showed = EXCLUDED.showed;' \
                           ''.format(keys_list, achieve_list_template)
        self.execute_query(insert_ach_query, values_list)

    def insert_iitc_achieve_check(self, data):
        """INSERT ACHIVE LIST"""
        if not data.get('team') == 'N' and data.get('health') > 0:
            return

        self.execute_query('UPDATE achive SET status = %s WHERE late6 = %s AND lnge6 = %s;',
                           ('N', data.get('latE6'), data.get('lngE6')))

    def insert_ada_achive(self, keys_list, values_list):
        """INSERT ACHIVE LIST"""
        if not values_list:
            return
        achieve_list_template = ','.join(['%s'] * len(values_list))
        insert_ach_query = 'INSERT INTO achive {0} VALUES {1} ' \
                           'ON CONFLICT ON CONSTRAINT achive_late6_lnge6_key DO UPDATE SET player = EXCLUDED.player,' \
                           ' team = EXCLUDED.team, timestamp = EXCLUDED.timestamp, name = EXCLUDED.name;' \
                           ''.format(keys_list, achieve_list_template)
        self.execute_query(insert_ach_query, values_list)

    def insert_iitc_guid(self, keys_list, values_list):
        """INSERT ACHIVE LIST"""
        if not values_list:
            return
        achieve_list_template = ','.join(['%s'] * len(values_list))
        insert_ach_query = 'INSERT INTO achive {0} VALUES {1} ' \
                           'ON CONFLICT ON CONSTRAINT achive_late6_lnge6_key DO UPDATE SET ' \
                           'name = EXCLUDED.name, pguid = EXCLUDED.pguid, img = EXCLUDED.img;' \
                           ''.format(keys_list, achieve_list_template)
        self.execute_query(insert_ach_query, values_list)

    def insert_iitc_achive(self, keys_list, values_list):
        """INSERT ACHIVE LIST"""
        if not values_list:
            return
        achieve_list_template = ','.join(['%s'] * len(values_list))
        insert_ach_query = 'INSERT INTO achive {0} VALUES {1} ' \
                           'ON CONFLICT ON CONSTRAINT achive_late6_lnge6_key DO UPDATE SET ' \
                           'name = EXCLUDED.name, pguid = EXCLUDED.pguid, img = EXCLUDED.img, team = EXCLUDED.team,' \
                           ' player = null;'.format(keys_list, achieve_list_template)
        self.execute_query(insert_ach_query, values_list)

    def get_portals_for_maxfield(self, arguments, limit=30):
        cLat = arguments['latlng'][0]
        cLng = arguments['latlng'][1]

        killer = 1
        if limit == 30:
            killer = 2

        select_query = "SELECT late6, lnge6, name FROM achive WHERE late6 > %s " \
                       "AND late6 < %s AND lnge6 > %s AND lnge6 < %s LIMIT %s;"

        args = (int(cLat - 6000/killer), int(cLat + 6000/killer),
                int(cLng - 12000/killer), int(cLng + 12000/killer), limit)
        return self.execute_query(select_query, args, )

    def get_achieve_by_latlng(self, arguments):
        import bot.util as util
        team = arguments['team']
        days = arguments['days']
        cLat = arguments['latlng'][0]
        cLng = arguments['latlng'][1]
        zoom = arguments['zoom']
        multiplier = util.zoom_area(zoom)
        attention = arguments.get('attention')
        user_checked = arguments.get('user_checked')

        if attention and user_checked:
            if team == 'all':
                select_query = "SELECT id, name, player, late6, lnge6, address, ada, timestamp, team, img, pguid " \
                               "FROM achive WHERE ((timestamp < %s AND timestamp > %s) OR (timestamp < %s AND timestamp > %s))" \
                               " AND late6 > %s AND late6 < %s AND " \
                               "lnge6 > %s AND lnge6 < %s AND (team = 1 OR team = 2) AND status IS NULL AND showed = false ORDER BY timestamp asc;"
                args = (attention['min_87'], attention['max_87'], attention['min_147'], attention['max_147'],
                        int(cLat - 2 * multiplier), int(cLat + 2 * multiplier),
                        int(cLng - 3 * multiplier), int(cLng + 3 * multiplier))
            else:
                select_query = "SELECT id, name, player, late6, lnge6, address, ada, timestamp, team, img, pguid " \
                               "FROM achive WHERE ((timestamp < %s AND timestamp > %s) OR (timestamp < %s AND timestamp > %s))" \
                               " AND late6 > %s AND late6 < %s AND " \
                               "lnge6 > %s AND lnge6 < %s AND team = %s AND status IS NULL AND showed = false ORDER BY timestamp asc;"
                args = (attention['min_87'], attention['max_87'], attention['min_147'], attention['max_147'],
                        int(cLat - 2 * multiplier), int(cLat + 2 * multiplier),
                        int(cLng - 3 * multiplier), int(cLng + 3 * multiplier), team)
        elif attention:
            if team == 'all':
                select_query = "SELECT id, name, player, late6, lnge6, address, ada, timestamp, team, img, pguid " \
                               "FROM achive WHERE ((timestamp < %s AND timestamp > %s) OR (timestamp < %s AND timestamp > %s))" \
                               " AND late6 > %s AND late6 < %s AND " \
                               "lnge6 > %s AND lnge6 < %s AND (team = 1 OR team = 2) AND showed = false ORDER BY timestamp asc;"
                args = (attention['min_87'], attention['max_87'], attention['min_147'], attention['max_147'],
                        int(cLat - 2 * multiplier), int(cLat + 2 * multiplier),
                        int(cLng - 3 * multiplier), int(cLng + 3 * multiplier))
            else:
                select_query = "SELECT id, name, player, late6, lnge6, address, ada, timestamp, team, img, pguid " \
                               "FROM achive WHERE ((timestamp < %s AND timestamp > %s) OR (timestamp < %s AND timestamp > %s))" \
                               " AND late6 > %s AND late6 < %s AND " \
                               "lnge6 > %s AND lnge6 < %s AND team = %s AND showed = false ORDER BY timestamp asc;"
                args = (attention['min_87'], attention['max_87'], attention['min_147'], attention['max_147'],
                        int(cLat - 2 * multiplier), int(cLat + 2 * multiplier),
                        int(cLng - 3 * multiplier), int(cLng + 3 * multiplier), team)

        elif user_checked:
            if team == 'all':
                select_query = "SELECT id, name, player, late6, lnge6, address, ada, timestamp, team, img, pguid" \
                               " FROM achive WHERE timestamp < %s " \
                               "AND late6 > %s AND late6 < %s AND " \
                               "lnge6 > %s AND lnge6 < %s AND (team = 1 OR team = 2) AND status IS NULL" \
                               " AND showed = false ORDER BY timestamp asc;"
                args = (util.TimeCl().past_from_days(int(days)), int(cLat - 2 * multiplier), int(cLat + 2 * multiplier),
                        int(cLng - 3 * multiplier), int(cLng + 3 * multiplier))
            else:
                select_query = "SELECT id, name, player, late6, lnge6, address, ada, timestamp, team, img, pguid" \
                               " FROM achive WHERE timestamp < %s " \
                               "AND late6 > %s AND late6 < %s AND " \
                               "lnge6 > %s AND lnge6 < %s AND team = %s AND status IS NULL AND showed = false ORDER BY timestamp asc;"
                args = (util.TimeCl().past_from_days(int(days)), int(cLat - 2 * multiplier), int(cLat + 2 * multiplier),
                        int(cLng - 3 * multiplier), int(cLng + 3 * multiplier), team)
        else:
            if team == 'all':
                select_query = "SELECT id, name, player, late6, lnge6, address, ada, timestamp, team, img, pguid" \
                               " FROM achive WHERE timestamp < %s " \
                               "AND late6 > %s AND late6 < %s AND " \
                               "lnge6 > %s AND lnge6 < %s AND (team = 1 OR team = 2) AND showed = false ORDER BY timestamp asc;"
                args = (util.TimeCl().past_from_days(int(days)), int(cLat - 2 * multiplier), int(cLat + 2 * multiplier),
                        int(cLng - 3 * multiplier), int(cLng + 3 * multiplier))
            else:
                select_query = "SELECT id, name, player, late6, lnge6, address, ada, timestamp, team, img, pguid" \
                               " FROM achive WHERE timestamp < %s " \
                               "AND late6 > %s AND late6 < %s AND " \
                               "lnge6 > %s AND lnge6 < %s AND team = %s AND showed = false ORDER BY timestamp asc;"
                args = (util.TimeCl().past_from_days(int(days)), int(cLat - 2 * multiplier), int(cLat + 2 * multiplier),
                        int(cLng - 3 * multiplier), int(cLng + 3 * multiplier), team)

        return self.execute_query(select_query, args)

    def get_portal_by_id(self, id):
        select_query = "SELECT * FROM achive WHERE id = %s;"
        args = (id, )
        return self.execute_query(select_query, args)

    def get_portal_by_latlng(self, arguments):
        late6 = arguments[0]
        lnge6 = arguments[1]

        select_query = "SELECT player, late6, lnge6, address, ada, timestamp, team FROM achive " \
                       "WHERE late6 = %s AND lnge6 = %s;"
        args = (late6, lnge6, )
        return self.execute_query(select_query, args, )

    def get_portals_in_area(self, latlng_with_delta, offset=0):
        late6 = latlng_with_delta[0]
        lnge6 = latlng_with_delta[1]
        deltalat = latlng_with_delta[2]
        deltalng = latlng_with_delta[3]

        select_query = "SELECT * FROM achive WHERE late6 > %s " \
                       "AND late6 < %s AND lnge6 > %s AND lnge6 < %s LIMIT 50 OFFSET %s;"

        count_query = "SELECT count(*) FROM achive WHERE late6 > %s " \
                      "AND late6 < %s AND lnge6 > %s AND lnge6 < %s;"

        count_args = (int(late6 - deltalat), int(late6 + deltalat),
                int(lnge6 - deltalng), int(lnge6 + deltalng))

        args = (int(late6 - deltalat), int(late6 + deltalat),
                int(lnge6 - deltalng), int(lnge6 + deltalng), offset)
        count = self.execute_query(count_query, count_args)
        portals = self.execute_query(select_query, args)
        return portals, count[0]

    def get_players_list_in_area(self, latlng_with_delta, offset=0):
        late6 = latlng_with_delta[0]
        lnge6 = latlng_with_delta[1]
        deltalat = latlng_with_delta[2]
        deltalng = latlng_with_delta[3]

        select_query = "SELECT DISTINCT ON (player) player FROM achive WHERE late6 > %s " \
                       "AND late6 < %s AND lnge6 > %s AND lnge6 < %s AND team = 2;"

        select_player_query = "SELECT DISTINCT ON (player) player FROM player WHERE late6 > %s " \
                              "AND late6 < %s AND lnge6 > %s AND lnge6 < %s AND team = 2;"

        args = (int(late6 - deltalat), int(late6 + deltalat),
                int(lnge6 - deltalng), int(lnge6 + deltalng))

        portals = self.execute_query(select_query, args)
        player = self.execute_query(select_player_query, args)
        return portals, player

    def get_portals_by_offset(self, offset, limit=50):
        select_query = "SELECT player, late6, lnge6, timestamp, ada, team, name, address FROM achive " \
                       "OFFSET %s LIMIT %s;"
        args = (offset, limit, )
        return self.execute_query(select_query, args,  )

    def get_achieve_by_player(self, arguments):
        player = arguments['args']['player']

        return self.execute_query("SELECT * FROM achive WHERE LOWER(player) = LOWER(%s)"
                                  " ORDER BY timestamp asc;", (player, ),)

    def get_no_pguid_portals(self):
        """For tiles create"""
        select_query = "SELECT late6, lnge6 FROM achive WHERE img is null OR img ~ 'panoramio' LIMIT 10000;"

        return self.execute_query(select_query,  )

    def get_no_pguid_portals_to_web(self, arguments):
        """DELETE IT"""
        faction = arguments['faction']
        latlng = arguments['latlng']
        cLat = latlng[0]
        cLng = latlng[1]
        """For tiles create"""
        select_query = "SELECT * FROM achive WHERE pguid IS NULL ORDER BY late6;"
        args = (int(cLat - 2*1E6), int(cLat + 2*1E6), int(cLng - 4*1E6), int(cLng + 4*1E6))
        return self.execute_query(select_query, args,)

    def get_images(self):
        select = "SELECT img, late6, lnge6 FROM achive WHERE img IS NOT NULL AND downloaded IS NULL " \
                 "AND img !='' LIMIT 10000;"

        return self.execute_query(select,)

    def image_insert(self, late6, lnge6, path):
        insert_query = "INSERT INTO achive (late6, lnge6, downloaded) VALUES (%s,%s,%s) ON CONFLICT ON CONSTRAINT " \
                       "achive_late6_lnge6_key DO UPDATE SET downloaded = EXCLUDED.downloaded;"

        insert_args = (late6, lnge6, path)
        self.execute_query(insert_query, insert_args)

    """Tiles"""
    def tile_update_portals(self, portals):
        if not portals:
            return
        portal_list_template = ','.join(['%s'] * len(portals))
        insert_ach_query = 'INSERT INTO achive (pguid, late6, lnge6, name, img, tile) VALUES {0} ' \
                           'ON CONFLICT ON CONSTRAINT achive_late6_lnge6_key DO UPDATE SET ' \
                           'name = EXCLUDED.name, pguid = EXCLUDED.pguid, img = EXCLUDED.img, tile = EXCLUDED.tile;' \
                           ''.format(portal_list_template)
        values = []
        for i in portals:
            values.append((i['pguid'], i['late6'], i['lnge6'], i['name'], i['img'], i['tile']))

        self.execute_query(insert_ach_query, values)


class PortalDetail(PostgreLocal):
    """Portal detail class"""
    def get_pd_list(self, task):
        return self.execute_query("SELECT achive.name, achive.pguid, achive.img, achive.address, inspector.*"
                                  " FROM inspector LEFT JOIN achive ON inspector.late6 = achive.late6 AND "
                                  "inspector.lnge6 = achive.lnge6 WHERE task = %s;", (task,),
                                   )

    def add_pd_portal(self, portal):
        insert_query = "INSERT INTO inspector (name, guid, expired, late6, lnge6, address, task, tag, parameters," \
                       " allow) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        args = (portal.get('name'), portal.get('pguid'), int(round(time.time() * 1000)), portal.get('late6'),
                portal.get('lnge6'), portal.get('address'), 'monitor', 'diff', 'any', 'monitor,')

        self.execute_query(insert_query, args)

    def delete_portal(self, pguid):
        self.execute_query("DELETE FROM inspector WHERE guid = %s", (pguid, ))

    def update_pd(self, pd):
        """INSERT PORTAL DETAILS"""
        insert_query = 'INSERT INTO inspector (guid, player, lvl, resonators, timestamp, mods, team) VALUES ' \
                       '(%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT inspector_guid_key DO UPDATE SET ' \
                       'player = EXCLUDED.player, lvl = EXCLUDED.lvl, ' \
                       'resonators = EXCLUDED.resonators, timestamp = EXCLUDED.timestamp, mods = EXCLUDED.mods, ' \
                       'team = EXCLUDED.team;'
        args = (pd.get('guid'), pd.get('player'), pd.get('lvl'), json.dumps(pd.get('resonators')), pd.get('timestamp'),
                json.dumps(pd.get('mods')), pd.get('team'))
        self.execute_query(insert_query, args)

    def get_portals_by_tag(self, tag):
        query = "SELECT * FROM inspector WHERE allow ~* %s;"
        arg = (tag, )
        return self.execute_query(query, arg,  )

    def get_allow_telegram_users(self, allow_list):
        """Get send to"""
        allow_users = []
        for i in allow_list:
            if not i:
                continue
            select_query = "SELECT chat_id FROM telegram WHERE approved = True AND chat_id = %s;"
            result = self.execute_query(select_query, (i,))

            if result:
                for r in result:
                    if r.get('chat_id') not in allow_users:
                        allow_users.append(r.get('chat_id'))
        return allow_users

    def portal_history(self, late6, lnge6):
        name = self.execute_query("SELECT name FROM achive WHERE late6 = %s AND lnge6 = %s;",
                                  (late6, lnge6))
        if name:
            portal = {'name': name}
            select_query = "SELECT * FROM actions WHERE late6 = %s AND lnge6 = %s ORDER BY timestamp DESC LIMIT 100;"
            args = (late6, lnge6)
            history = PostgreLocal().execute_query(select_query, args,  )
            portal.update({'history': history})
            return portal
        return {'error': 'portal not found in DB'}

    def find_address_by_geo(self, late6, lnge6):
        result = self.execute_query("SELECT address FROM achive WHERE late6 < %s AND late6 > %s AND lnge6 "
                                    "< %s AND lnge6 > %s LIMIT 1;", (late6 + 100000, late6 - 100000, lnge6 + 100000,
                                                                     lnge6 - 100000),)
        return result


class ShortUrl(PostgreLocal):
    def get_url(self, url):
        return self.execute_query("SELECT * FROM short_url WHERE s_url = %s;", (url,),
                                             )

    def write_url(self, url):
        insert_query = "INSERT INTO short_url (url, s_url) VALUES (%s,%s) RETURNING *;"
        args = (url, str(uuid.uuid4())[:6])
        short_url = self.execute_query(insert_query, args,  )

        return short_url


class Admin(PostgreLocal):
    """Admin interface"""
    def create_user(self, **kwargs):
        from bot.util import token
        if not self.execute_query("SELECT email FROM accounts WHERE email = %s;", (kwargs['email'], )):
            self.execute_query("INSERT INTO accounts (email, gender, name, given_name, picture,"
                               " verified_email, family_name, link, permissions, token) "
                               "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                               "", (kwargs['email'], kwargs.get('gender'), kwargs.get('name'),
                               kwargs.get('given_name'), kwargs.get('picture'), kwargs['verified_email'],
                               kwargs.get('family_name'), kwargs.get('link'), 'all', token()))

    def get_user(self, username):
        result = self.execute_query("SELECT email, verified_email, permissions, token FROM accounts WHERE email = %s",
                                    (username,),  )
        if result:
            return result[0]
        return {'error': 'user don`t exist'}

    def get_user_by_token(self, token):
        result = self.execute_query("SELECT * FROM accounts WHERE token = %s", (token, ))
        if result:
            return result[0]

    def set_gname_by_token(self, gname, token):
        self.execute_query("UPDATE accounts SET gname = %s WHERE token = %s;", (gname, token, ))

    def get_players(self, player):
        return self.execute_query("SELECT * FROM player WHERE player_lowercase ~ %s"
                                  " ORDER BY player asc;", (player.lower(), ))

    def get_telegram_user_by_name(self, user):
        if type(user) is int:
            result = self.execute_query("SELECT * FROM accounts WHERE telegram_name = %s;", (str(user), ),
                                         )
        else:
            result = self.execute_query("SELECT * FROM accounts WHERE telegram_name = %s;", (user, ),
                                         )
        if result:
            return result[0]
        return {'error': 'telegram user not found!'}

    def create_telegram_user(self, username, chat_id, is_group=False):
        self.execute_query("INSERT INTO telegram (username, chat_id, is_group) VALUES (%s,%s,%s) ON CONFLICT ON "
                           "CONSTRAINT telegram_chat_id_key DO UPDATE SET chat_id = EXCLUDED.chat_id, "
                           "is_group = EXCLUDED.is_group;", (username, chat_id, is_group))

    def get_telegram_user(self, id):
        result = self.execute_query("SELECT * FROM telegram WHERE chat_id = %s;", (id, ),
                                     )
        if result:
            return result[0]
        return None

    def get_gname_by_telegram_user(self, user):
        result = self.execute_query("SELECT gname FROM accounts WHERE telegram_name = %s;", (user, ),
                                     )
        if result:
            return result[0]
        return {'error': 'argument needed!'}

    "User logging"
    def write_user_log(self, request, user):
        self.execute_query("INSERT INTO userslog (action, email, timestamp, ip, data) "
                           "VALUES (%s,%s,%s,%s,%s);",
                           (request.get('request'), user.get('email'), int(round(time.time() * 1000)),
                            request.get('user_ip'), json.dumps(request)))

    def get_user_log(self):
        return self.execute_query("SELECT * FROM userslog ORDER BY timestamp desc LIMIT 1000;", )


class ScannerPg(PostgreLocal):
    def insert_profile(self, profile):
        insert_query = "INSERT INTO profiles (playername, lvl, team, badges, metrics, ap, mission_badges, update) " \
                       "VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"

        args = (profile['playername'], profile['lvl'], profile['team'], json.dumps(profile['badges']), json.dumps(profile['metrics']),
                profile['ap'], json.dumps(profile['mission_badges']), profile['update'])
        self.execute_query(insert_query, args)

        insert_guardian = "INSERT INTO players (low_name, guardian) VALUES (%s,%s) ON CONFLICT ON CONSTRAINT" \
                          " players_low_name_key DO UPDATE SET guardian = EXCLUDED.guardian;"
        guard_args = (profile['playername'].lower(), profile['guardian'])
        self.execute_query(insert_guardian, guard_args)

    def insert_error_profile(self, player):
        self.execute_query("INSERT INTO profiles (playername, update) VALUES (%s,%s)",
                           (player, int(round(time.time() * 1000))))

    def get_profile(self, player):
        profile = self.execute_query("SELECT * FROM profiles WHERE playername = %s ORDER BY update DESC LIMIT 1;",
                                     (player, ),  )
        if profile:
            return profile[0]

    """proxy data"""
    def update_agent_info(self, agent_name, agent_id, xsrf, faction):
        self.execute_query("UPDATE scanner_player_id SET agent_id = %s, xsrf = %s, faction = %s, timestamp = %s WHERE agent_name = %s",
                           (agent_id, xsrf, faction, int(round(time.time() * 1000)), agent_name.lower()), )

    def update_agent_cookies(self, cookies, xsrf):
        self.execute_query("UPDATE scanner_player_id SET cookie = %s WHERE xsrf = %s", (cookies, xsrf, ), )

    def update_agent_inventory(self, data, agent_id):
        """INSERT ITEMS LIST"""
        if not data or not agent_id:
            return

        self.execute_query('INSERT INTO scanner_inventory (agent_id, description, timestamp) VALUES (%s, %s, %s) '
                           'ON CONFLICT ON CONSTRAINT scanner_inventory_agent_id_key DO '
                           'UPDATE SET agent_id = EXCLUDED.agent_id, description = EXCLUDED.description, '
                           'timestamp = EXCLUDED.timestamp;',
                           (agent_id, json.dumps(data), int(round(time.time() * 1000)), ), )

    def get_user_accounts(self, email):
        return self.execute_query("SELECT agent_name, agent_id, timestamp, faction, active"
                                  " FROM scanner_player_id WHERE email = %s", (email, ), )

    def add_account(self, agent_name, email):
        if not agent_name:
            return
        agents = self.execute_query("SELECT agent_name, agent_id, timestamp, faction, active"
                                    " FROM scanner_player_id WHERE email = %s", (email, ), )
        if len(agents) > 4:
            return {'error': 'reached limit of accounts'}
        try:
            if len(agents) == 0:
                self.execute_query("INSERT INTO scanner_player_id (email, agent_name, active)"
                                   " VALUES (%s,%s,%s);", (email, agent_name.lower(), True, ), )
            else:
                self.execute_query("INSERT INTO scanner_player_id (email, agent_name)"
                                   " VALUES (%s,%s);", (email, agent_name.lower(), ), )
        except psycopg2.IntegrityError:
            return {'error': 'this nickname already exists'}

        agents = self.execute_query("SELECT agent_name, agent_id, timestamp, faction, active"
                                    " FROM scanner_player_id WHERE email = %s", (email, ), )
        return agents

    def remove_account(self, agent_id, email):
        if not agent_id:
            return
        try:
            self.execute_query("DELETE FROM scanner_player_id WHERE agent_name = %s AND email = %s;", (agent_id, email, ), )
        except psycopg2.IntegrityError:
            return {'error': 'Server error'}

        agents = self.execute_query("SELECT agent_name, agent_id, timestamp, faction, active"
                                    " FROM scanner_player_id WHERE email = %s", (email, ), )
        return agents

    def hide_achievements(self, agent_id, email):
        import bot.util as util
        agent = self.execute_query("SELECT * FROM scanner_player_id WHERE email = %s AND agent_id = %s;",
                                   (email, agent_id,), )
        if not agent:
            return {'error': 'Server error'}

        timestamp = agent[0].get('hide')
        if timestamp:
            if util.TimeCl(int(timestamp)).daydiff() < 30:
                return {'error': 'You can hide it at {} again'.format(util.TimeCl(int(timestamp) + 2592000000).humans())}

        name = agent[0].get('agent_name')
        if not name:
            return {'error': 'Agent name not found'}

        self.execute_query("UPDATE achive SET showed = True WHERE LOWER(player) = LOWER(%s)", (name, ))
        self.execute_query("UPDATE scanner_player_id SET hide = %s WHERE agent_name = %s;",
                           (int(round(time.time() * 1000)), name,))
        agents = self.execute_query("SELECT agent_name, agent_id, timestamp, faction, active"
                                    " FROM scanner_player_id WHERE email = %s", (email, ), )
        return agents

    def set_active(self, agent_id, email):
        agents = self.execute_query("SELECT agent_name, agent_id, timestamp, faction, active"
                                    " FROM scanner_player_id WHERE email = %s", (email, ), )
        for i in agents:
            print(i)

    def get_agent_inventory(self, agent_id):
        return self.execute_query("SELECT description, timestamp FROM scanner_inventory WHERE agent_id = %s;", (agent_id, ), )


class PlayerPg(PostgreLocal):
    def find_player(self, player):
        if len(player) < 3:
            return {'error': 'short name'}

        result = self.execute_query("SELECT DISTINCT ON (player) player, team FROM achive WHERE player ~* %s ORDER BY "
                                    "player DESC;", (player, ),)

        if not result:
            result = PostgreLocal().execute_query("SELECT DISTINCT ON (player) player FROM actions WHERE "
                                                   "player ~* %s ORDER BY player DESC;",
                                                   (player, ),  )
        return result

    def get_all_users_to_list(self):
        return self.execute_query("SELECT DISTINCT ON (player) player FROM achive;")

    def player_from(self, player):
        select_query = "SELECT * FROM players WHERE low_name = %s;"
        args = (player, )
        result = self.execute_query(select_query, args,  )
        if result:
            return result[0]
        return result

    def create_player_statistics(self, query):
        insert_query = "INSERT INTO players (player, low_name, late6, lnge6, live_in, update) " \
                       "VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT players_low_name_key " \
                       "DO UPDATE SET late6 = EXCLUDED.late6, lnge6 = EXCLUDED.lnge6, live_in =" \
                       " EXCLUDED.live_in, update = EXCLUDED.update;"
        args = (query['player'], query['player'].lower(), query['late6'], query['lnge6'], query['live_in'],
                int(round(time.time() * 1000)))
        self.execute_query(insert_query, args)
        return
