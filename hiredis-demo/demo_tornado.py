# !/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-3-7


import asyncio

import aioredis
from tornado import gen


@gen.coroutine
def main():
    redis = yield aioredis.create_redis('redis://localhost')

    # No pipelining;
    @gen.coroutine
    def wait_each_command():
        val = yield redis.get('foo')  # wait until `val` is available
        cnt = yield redis.incr('bar')  # wait until `cnt` is available

        return gen.Return((val, cnt))

        # Sending multiple commands and then gathering results

    # async def pipelined():
    #     fut1 = redis.get('foo')  # issue command and return future
    #     fut2 = redis.incr('bar')  # issue command and return future
    #     # block until results are available
    #     val, cnt = yield asyncio.gather(fut1, fut2)
    #     return val, cnt

    # Explicit pipeline
    @gen.coroutine
    def explicit_pipeline():
        pipe = redis.pipeline()
        fut1 = pipe.get('foo')
        fut2 = pipe.incr('bar')
        result = yield pipe.execute()
        val, cnt = yield asyncio.gather(fut1, fut2)
        assert result == [val, cnt]
        return gen.Return((val, cnt))

    res = yield wait_each_command()
    print(res)
    # res = yield pipelined()
    # print(res)
    res = yield explicit_pipeline()
    print(res)

    redis.close()
    yield redis.wait_closed()


if __name__ == '__main__':
    import tornado
    from tornado import ioloop

    loop = tornado.ioloop.IOLoop.current()
    loop.run_sync(main)
