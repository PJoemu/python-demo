#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:12/04/18
import typing


class LruCache(object):

    def __init__(self, capacity=100):
        self.__key_map = dict()
        self.__capacity = capacity

    def get(self, key: str) -> typing.Optional[str]:
        ret_value = None
        if key in self.__key_map:
            ret_value = self.__key_map.pop(key)
            self.__key_map[key] = ret_value
        return ret_value

    def set(self, key, value):
        key_list = list(self.__key_map.keys())
        if len(key_list) >= self.__capacity:
            self.__key_map.pop(key_list[0])

        if key in self.__key_map:
            del self.__key_map[key]
        self.__key_map[key] = value

    def delete(self, key: str):
        if key in self.__key_map:
            del self.__key_map[key]

    @property
    def capacity(self):
        return self.__capacity

    @property
    def key_map(self):
        return self.__key_map


if __name__ == '__main__':
    lru = LruCache()
    lru.set('a', 'a')
    lru.set('b', 'b')
    lru.set('c', 'c')

    pass
