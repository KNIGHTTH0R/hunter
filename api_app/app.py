import sys

sys.path.append('./')

from api_app.handlers import *
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.autoreload
import tornado.httpserver
import tornado.websocket
from tornado import web
from tornado.options import define, options
from api_app.controller import *


define("port", default=8888, help="run on the given port", type=int)
define("debug", default=settings.DEBUG, help='enable debug mode', type=bool)
define("google_key", default=settings.GOOGLE_KEY, help='enable debug mode', type=str)
define("google_secret", default=settings.GOOGLE_SECRET, help='enable debug mode', type=str)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r'/api', ApiHandler),
            (r'/api/user', UserHandler),
            (r'/version', GetVersionHandler),
            (r'/login', AuthLoginHandler),
            (r"/auth/login/", GAuthLoginHandler),
            (r"/auth/logout/", AuthLogoutHandler),
            (r'/plugins/([a-zA-Z0-9.-].*)achievements_plugin.user.js', GetPluginNotAuthHandler),
            (r'/plugins/([a-zA-Z0-9.-].*)achievements_plugin.meta.js', GetPluginMetaNotAuthHandler),
            (r'/plugins/achievements_plugin.user.js', GetPluginHandler),
            # (r'/map', TestHandler),
            # (r'/ws', WebSocket),
            (r'/(.*)', StaticFileHandler, {'path': 'api_app/static/', 'default_filename': 'index.html'}),
        ]
        settings = dict(
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            template_path=os.path.join(os.path.dirname(__file__), "static"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug=options.debug,
            login_url="/login",
            google_oauth={'key': options.google_key,
                          'secret': options.google_secret}
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class StaticFileHandler(tornado.web.StaticFileHandler):
    def data_received(self, chunk):
        pass

    def post(self, *args, **kwargs):
        self.redirect('/')


if __name__ == "__main__":
    if settings.DEBUG:
        tornado.options.parse_command_line()
        app = Application()
        app.listen(options.port)
        tornado.ioloop.IOLoop.current().start()
    else:
        app = Application()
        server = tornado.httpserver.HTTPServer(app)
        server.bind(8888)
        server.start(0)
        tornado.ioloop.IOLoop.instance().start()