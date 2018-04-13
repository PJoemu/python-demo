#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:13/04/18
import json

from jwt import ExpiredSignatureError
from tornado import web, gen
from mixin import RenderMixin
from util import JwtHelper


class BaseRequestHandler(web.RequestHandler, RenderMixin):
    def data_received(self, chunk):
        pass


class HelloHandler(BaseRequestHandler):
    @gen.coroutine
    def get(self):
        self.write({
            'msg': 'success'
        })
        self.finish()


class LoginHandler(BaseRequestHandler):
    def post(self, *args, **kwargs):
        json_data = json.loads(self.request.body.decode('utf-8'))
        username = json_data.get('username', None)
        password = json_data.get('password', None)
        if not username or not password:
            self.render_error("param error")
            return
        user_info = {
            'username': username
        }
        _, token = JwtHelper.gen_token(user_info)

        ret_data = {
            'token': str(token)
        }
        self.render_success(ret_data)

    def get(self, *args, **kwargs):
        token_arg = self.get_argument('token', '')
        token_header = self.request.headers.get("Authorization")
        token_header = token_header.split(':')[1]

        token = token_arg or token_header
        payload, err = JwtHelper.parse_token(token)
        if err is ExpiredSignatureError:
            self.render_error('ExpiredSignatureError')
            return

        self.render_success(payload)
