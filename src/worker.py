# -*- coding: utf-8 -*-

import asyncio

class AbstractWorker(object):

    def __init__(self, inp, out):
        self._input = inp
        self._output = out
        self._close = False

    def __call__(self):
        asyncio.ensure_future(self.work())

    def close(self):
        self._close = True

    def is_closed(self):
        return self._close

    async def work(self):
        while True:
            item = await self._input.get()

            if (self._close):
                break

            task = asyncio.ensure_future(self.process_next(item))
            task.add_done_callback(self.complete_callback)

    def complete_callback(self, f):
        
        async def complete_worker(item):
            await self._output.put(item)

        asyncio.ensure_future(complete_worker(f.result()))


    async def process_next(self, item):
        return item