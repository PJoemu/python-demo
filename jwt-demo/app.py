#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:09/04/18
import logging

import tornado
from tornado import ioloop
from tornado import web
from tornado import options
from tornado.options import define, options, parse_command_line

import handler

define("port", default=7777, help="Run server on a specific port", type=int)


class Application(web.Application):

    def __init__(self):
        handler_list = [
            (r'/hello', handler.HelloHandler),
            (r'/user', handler.LoginHandler),
        ]
        settings = dict(
            debug=True,

        )
        web.Application.__init__(self, handler_list, **settings)


def start_server():
    options.logging = 'debug'
    logging.basicConfig(level=logging.INFO)
    app = Application()
    parse_command_line()
    app.listen(options.port)

    loop = ioloop.IOLoop().current()
    try:
        logging.info('Tornado version {}'.format(tornado.version))
        logging.info('Tornado Server Start, listen on {}'.format(options.port))
        logging.info('Quite the Server with CONTROL-C.')
        loop.start()
    except KeyboardInterrupt:
        loop.close()


if __name__ == '__main__':
    start_server()
