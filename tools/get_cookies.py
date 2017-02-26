#!/usr/bin/env python
# -*- encode: utf-8 -*-
import sys
sys.path.append('./')

import re
import settings
import cookielib
import mechanize
import time
from datetime import datetime, timedelta
import psycopg2
import os


class SelfMongo():
    pgdb = psycopg2.connect(settings.PSQL_PRIMARY)

    def select_query(self, query):
        cur = self.pgdb.cursor()
        cur.execute(query)
        return cur.fetchall()

    def update_row(self, query):
        cur = self.pgdb.cursor()
        cur.execute(query)
        self.pgdb.commit()


class TimeCl(object):
    def __init__(self, timestamp):
        self.seconds, self.millis = divmod(timestamp, 1000)
        self.tsnow = datetime.now()
        self.timediff = self.tsnow - datetime.fromtimestamp(self.seconds)

    def daydiff(self):
        return self.timediff.days

    def secdiff(self):
        return self.timediff.seconds

    def mindiff(self):
        return round(self.timediff.seconds / 60)


class CookiesUpdate(object):
    def __init__(self, email, passwd):
        self.email = email
        self.passwd = passwd
        self.current_milli_time = int(round(time.time() * 1000))

    def get_cookie(self):
        cj = cookielib.LWPCookieJar()
        browser = mechanize.Browser()
        browser.set_cookiejar(cj)
        browser.set_handle_robots(False)
        browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        browser.open('http://ingress.com/intel')

        for link in browser.links(url_regex='ServiceLogin'):
            browser.follow_link(link)
            browser.select_form(nr=0)
            browser.form['Email'] = self.email
            browser.submit()
            browser.select_form(nr=0)
            browser.form['Passwd'] = self.passwd
            browser.submit()
            try:
                browser.select_form(nr=0)
                browser.submit()
            except Exception as e:
                print(e)
        return cj

    def parse_cookie(self):
        a = ''
        for i in self.get_cookie():
            if settings.DEBUG:
                print(i.name, i.value)
            if i.name == 'SACSID' or i.name == 'csrftoken':
                a = a + i.name + '=' + i.value + '; '

        self.update_new_cookie(a)

    def update_last_access(self):
        update_data = "UPDATE cookies SET " \
                      "status = 'ok', lastaccess = {} " \
                      "WHERE email = '{}';".format(self.current_milli_time, self.email)
        if settings.DEBUG:
            print(update_data)
        SelfMongo().update_row(update_data)

    def update_new_cookie(self, cookie):
        update_data = "UPDATE cookies SET " \
                      "status = 'ok', cookie = '{}', lastupdate = {}, lastaccess = {} " \
                      "WHERE email = '{}';".format(cookie, self.current_milli_time, self.current_milli_time, self.email)
        SelfMongo().update_row(update_data)


def psql_to_json(schema, result):
    json_word = {}
    for idx, val in enumerate(schema):
        json_word.update({val: result[idx]})
    return json_word


def set_cookie():
    schema = ('email', 'passwd', 'lastaccess', 'lastupdate', 'status')
    result = SelfMongo().select_query("SELECT email, passwd, lastaccess, lastupdate, status FROM cookies;")

    for i in result:
        i = psql_to_json(schema, i)
        try:
            if settings.DEBUG:
                print(TimeCl(i['lastaccess']).mindiff())
            if TimeCl(i['lastupdate']).daydiff() > 0 or i['status'] == 'error':
                CookiesUpdate(i['email'], i['passwd']).parse_cookie()
                break
            elif TimeCl(i['lastaccess']).secdiff() > 30:
                CookiesUpdate(i['email'], i['passwd']).update_last_access()
            else:
                if settings.DEBUG:
                    print('GetCookies: No errors and oldest in ' + i['email'])
        except KeyError:
            CookiesUpdate(i['email'], i['passwd']).parse_cookie()


while True:
    set_cookie()
    time.sleep(10)