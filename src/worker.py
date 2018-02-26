# -*- coding: utf-8 -*-


class AbstractWorker(object):

    def __init__(self, inp, out):
        self._input = inp
        self._output = out
        self._close = False

    async def close(self):
        self._close = True

    def is_closed(self):
        return self._close

    async def work(self):
        while True:
            item = await self._input.get()

            if (self._close):
                break

            await self._output.put(await process_next(item))


    async def process_next(self, item):
        return item