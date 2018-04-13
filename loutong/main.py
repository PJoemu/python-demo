#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-3-16
import uuid

import redis
import time
import logging
import threading

logging.basicConfig(level=logging.INFO)
Redis_Config = {
    'host': '127.0.0.1'
}


class RedisConnection(object):
    CONNECTION_POOL = redis.ConnectionPool(**Redis_Config)
    _client = None

    @classmethod
    def load_cache(cls) -> redis.Redis:
        if not cls._client:
            cls._client = redis.Redis(connection_pool=cls.CONNECTION_POOL)

        return cls._client


client = RedisConnection.load_cache()
host_token = str(uuid.uuid4())
event = threading.Event()
logging.info('host_token: %s' % host_token)


class SearchHost(object):

    def __init__(self):
        self.client = client
        self.host_token = host_token
        self.search_host_key = 'search_host'
        self.lou_tong_event = event
        self.is_work = False

    def keep_one_alive(self):
        pipe = self.client.pipeline()
        pipe.set(self.search_host_key, host_token)
        pipe.expire(self.search_host_key, 10)
        pipe.execute()

    def _search_host_exists(self):
        is_exists = self.client.get(self.search_host_key)
        logging.info('search host is_exists: %s' % is_exists)
        return True if is_exists else False

    def run_host_exists(self):
        while 1:
            if not self._search_host_exists():
                logging.info('search_host_exists not exist...')
                self.lou_tong_event.set()
                self.is_work = True
            time.sleep(8)

    def run(self):
        while 1:
            if self.is_work:
                self.keep_one_alive()

            time.sleep(5)


def lou_tong_start():
    event.wait()
    logging.info('lou_tong_start start...')
    while 1:
        token = str(uuid.uuid4())
        if client.llen('search_token') >= 100:
            logging.info('.')
            time.sleep(1)
            continue
        search_token = client.lpush('search_token', token)
        logging.info('token: %s---> total： %d' % (token, search_token))

        time.sleep(0.1)


if __name__ == '__main__':
    search_host_obj = SearchHost()
    thread_lou_tong_start = threading.Thread(target=lou_tong_start)
    thread_run = threading.Thread(target=search_host_obj.run)
    thread_run_host_exists = threading.Thread(target=search_host_obj.run_host_exists)
    thread_lou_tong_start.start()
    thread_run.start()
    thread_run_host_exists.start()
