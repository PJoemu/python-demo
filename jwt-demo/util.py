#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:13/04/18
import time

import jwt
from jwt import ExpiredSignatureError


class JwtHelper(object):
    SECRET = "arhieason"
    ALG = 'HS256'

    @classmethod
    def gen_token(cls, payload: dict) -> (bool, str):
        new_payload = {
            "iss": "arhieason.com",
            "iat": int(time.time()),
            "exp": int(time.time()) + 100000000,
        }
        new_payload.update(payload)

        token = jwt.encode(new_payload, cls.SECRET, algorithm=cls.ALG)
        return True, token

    @classmethod
    def parse_token(cls, token_str) -> (dict, Exception):
        try:
            payload = jwt.decode(token_str, cls.SECRET, algorithms=[cls.ALG])
        except ExpiredSignatureError as e:
            return dict(), ExpiredSignatureError
        if payload:
            return payload, None
        return dict(), None
