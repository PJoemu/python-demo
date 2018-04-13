#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-3-30

from tornado import web


class RenderMixin(object):

    def render_success(self: web.RequestHandler, data):
        ret_result = {
            'code': 0,
            'data': data,
            'status': 'success'
        }
        self.write(ret_result)
        self.finish()

    def render_error(self: web.RequestHandler, msg):
        ret_result = {
            'code': 500,
            'msg': msg,
            'status': 'error'
        }
        self.write(ret_result)
        self.finish()
