import sys
import threading

import redis

sys.path.append('./')

from api_app.handlers import *
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.autoreload
import tornado.httpserver
import tornado.websocket
from tornado import web
from functools import partial
from tornado.options import define, options
from api_app.controller import *


define("port", default=8887, help="run on the given port", type=int)
define("debug", default=settings.DEBUG, help='enable debug mode', type=bool)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', TestHandler),
            (r'/ws', WebSocket),
        ]
        settings = dict(
            cookie_secret="secret",
            template_path=os.path.join(os.path.dirname(__file__), "static"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=options.debug,
         )
        tornado.web.Application.__init__(self, handlers, **settings)


CONNECTED_CLIENTS = []


def redis_listener():
    r = redis.Redis(host='localhost', db=10)
    ps = r.pubsub()
    ps.subscribe('logs')
    io_loop = tornado.ioloop.IOLoop.instance()
    for message in ps.listen():
        for element in CONNECTED_CLIENTS:
            io_loop.add_callback(partial(element.on_message, message))


class WebSocket(tornado.websocket.WebSocketHandler):
    cache = []
    cache_size = 400

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    def open(self):
        CONNECTED_CLIENTS.append(self)
        for i in self.cache:
            self.write_message(i)

    def on_message(self, message):
        self.write_message(message['data'].decode('UTF-8'))

    def on_close(self):
        CONNECTED_CLIENTS.remove(self)
        print("WebSocket closed")

    def broadcast(self, pkg, all_but=None):
        for c in CONNECTED_CLIENTS:
            if c.join_completed and c != all_but:
                c.write_message(pkg)


if __name__ == "__main__":
    threading.Thread(target=redis_listener).start()
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
