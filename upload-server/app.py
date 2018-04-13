#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:09/04/18
import logging
import time

import tornado
from tornado import httputil
from tornado import ioloop, gen
from tornado import options
from tornado import web
from tornado.options import define, options, parse_command_line

UPLOAD_DIR = 'public'
define("port", default=8181, help="Run server on a specific port", type=int)


def save_file(file: httputil.HTTPFile, file_path):
    with open(file_path, 'wb+') as f:
        f.write(file.body)


class UploadHandler(web.RequestHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        file = self.request.files.get('file')[0]  # type: httputil.HTTPFile
        now = time.time()
        file_path = "%s/%s_%s" % (UPLOAD_DIR, file.filename, now)
        save_file(file, file_path)
        self.write("%s upload success." % file_path)
        self.finish()


class HelloHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.write({
            'msg': 'success'

        })
        self.finish()


class Application(web.Application):

    def __init__(self):
        handler_list = [
            (r'/upload', UploadHandler),
            (r'/hello', HelloHandler),
        ]
        settings = dict(
            debug=True,

        )
        web.Application.__init__(self, handler_list, **settings)


def start_server():
    options.logging = 'info'
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
