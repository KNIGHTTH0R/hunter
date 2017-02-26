import functools
import json
import re

import tornado
import os, sys

import tornado.template as template

from db.redisdb import RedisIpCheck

sys.path.append('./')
import settings
from bot.parser import IITCParser
from db.postgredb import Admin
from api_app.controller import ApiController
from api_app.models import PlayerModel
from tornado import gen, web, auth


def is_authenticated(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = None
        gname = None

        try:
            token = tornado.escape.json_decode(self.request.body).get('token', None)
            gname = tornado.escape.json_decode(self.request.body).get('iitc_player', None)
        except:
            token = None

        if self.get_secure_cookie('ingress-guard'):
            result = Admin().get_user(self.get_secure_cookie('ingress-guard').decode('UTF-8'))
        else:
            if token:
                result = Admin().get_user_by_token(token)

        if token == settings.TOKEN_API:
            self.current_user = True
        elif result:
            if result.get('gname') == 'new' and gname and token:
                Admin().set_gname_by_token(gname, token)
            self.current_user = result
        else:
            self.current_user = False
            self.clear_cookie("ingress-guard")
            self.redirect(self.get_argument("next", "/"))

        return func(self, *args, **kwargs)
    return wrapper


class BaseHandler(tornado.web.RequestHandler):
    def ip_check(self):
        if RedisIpCheck.check_ip(self.request.headers.get("X-Real-IP")):
            self.write({'error': 'So many requests from ip {}'.format(self.request.headers.get("X-Real-IP"))})
        else:
            return True

    def get_current_user(self):
        user = self.get_secure_cookie('ingress-guard')
        if not user:
            return None
        return True


class MainHandler(BaseHandler):
    @gen.coroutine
    def get(self, **kwargs):
        self.render("index.html")


class TestHandler(BaseHandler):
    @gen.coroutine
    def get(self, **kwargs):
        self.render("main.html")


class GetPluginHandler(BaseHandler):
    @is_authenticated
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        if self.ip_check():
            token = self.current_user.get('token')
            self.set_header("Content-Type", "text/plain")
            self.render("plugin_user.html", token=token)


class GetPluginNotAuthHandler(BaseHandler):
    @gen.coroutine
    def get(self, slug):
        if self.ip_check():
            if Admin().get_user_by_token(slug):
                self.set_header("Content-Type", "text/plain")
                self.render("plugin_user.html", token=slug)
            else:
                self.set_status(404)

class GetPluginMetaNotAuthHandler(BaseHandler):
    @gen.coroutine
    def get(self, slug):
        if self.ip_check():
            if Admin().get_user_by_token(slug):

                self.set_header("Content-Type", "text/plain")
                self.render("plugin_meta.html", token=slug)


class GetVersionHandler(BaseHandler):
    def get(self):
        plugin = open('api_app/static/plugin_user.html').readlines()
        for i in plugin:
            version = re.findall('// @version[ ]*([0-9.].*)', i)
            if version:
                version = {'v': version[0]}
                break
        self.write(version)


class ApiHandler(BaseHandler):
    """Main Api Handler"""
    @is_authenticated
    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        data.update({'user_ip': self.request.headers.get("X-Real-IP")})
        if data.get('token') == settings.TOKEN_API:
            self.write(ApiController(data, self.current_user).render())
        elif self.ip_check():
            self.write(ApiController(data, self.current_user).render())

    @tornado.web.authenticated
    @is_authenticated
    @gen.coroutine
    def get(self, **kwargs):
        if self.ip_check():

            requests = []
            for i in ApiController.actions:
                try:
                    requests.append(ApiController.actions[i].DESCRIPTION)
                except:
                    pass

            self.render("api.html", requests=requests)


class PlayerHandler(BaseHandler):
    """Main Api Handler"""
    # @tornado.web.authenticated
    # @is_authenticated
    @gen.coroutine
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        self.write(ApiController(data, self.current_user).render())

    def get(self):
        self.set_status(400)


class TelegramHandler(BaseHandler):
    """Main Api Handler"""
    @gen.coroutine
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        token = data.get('token')
        user = data.get('user')
        if token == settings.TOKEN_API and user:
            current = Admin().get_telegram_user_by_name(user)
            if current.get('error'):
                self.set_status(403)
            else:
                self.write(ApiController(data, current).render())
        else:
            self.set_status(403)

    def get(self):
        self.set_status(404)


class UserHandler(BaseHandler):
    """Main User Handler"""
    def post(self):
        self.set_status(400)

    @tornado.web.authenticated
    @is_authenticated
    @gen.coroutine
    def get(self):
        self.write(PlayerModel({}, self.current_user).user())


class GrubberFromIntel(tornado.web.RequestHandler):
    # @tornado.web.authenticated
    # @is_authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.set_status(404)

    def post(self, *args, **kwargs):
        guid = self.get_argument('guid')
        data = json.loads(self.get_argument('data'))
        if guid == 'iitc':
            IITCParser().to_redis(data)
        self.set_status(200)


# class MfHandler(BaseHandler):
#     """Main Api Handler"""
#     @gen.coroutine
#     def get(self):
#         if self.ip_check():
#             pass
#
#         late6 = self.get_arguments('late6')
#         lnge6 = self.get_arguments('lnge6')
#         tolist = self.get_arguments('tolist')
#         manual = self.get_arguments('manual')
#
#         if late6 and lnge6:
#             try:
#                 stats, result = MFController().render(late6[0], lnge6[0], tolist, manual)
#                 self.render("mfgenerator.html", stats=stats, result=result)
#             except:
#                 self.render("mfgenerator.html", stats='<p>Cant`t found portals in area or invalid arguments, '
#                                                       'try other location</p>', result=None)
#
#         else:
#             self.render("mfgenerator.html", stats=None, result=None)


class GAuthLoginHandler(tornado.web.RequestHandler, tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_current_user():
            self.redirect('/')
            return

        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(redirect_uri=settings.google_redirect_url,
                code=self.get_argument('code'))
            if not user:
                self.clear_all_cookies()
                raise tornado.web.HTTPError(500, 'Google authentication failed')

            access_token = str(user['access_token'])
            http_client = self.get_auth_http_client()
            response =  yield http_client.fetch('https://www.googleapis.com/oauth2/v1/userinfo?access_token='+access_token)
            if not response:
                self.clear_all_cookies()
                raise tornado.web.HTTPError(500, 'Google authentication failed')
            user = json.loads(response.body.decode('UTF-8'))
            Admin().create_user(**user)
            self.set_secure_cookie('ingress-guard', user['email'])
            self.redirect('/')
            return

        elif self.get_secure_cookie('ingress-guard'):
            self.redirect('/auth/login/')
            return

        else:
            yield self.authorize_redirect(
                redirect_uri=settings.google_redirect_url,
                client_id=self.settings['google_oauth']['key'],
                scope=['email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})


class AuthLoginHandler(BaseHandler):
    def get(self):
        self.render("auth.html")


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("ingress-guard")
        self.redirect(self.get_argument("next", "/"))
