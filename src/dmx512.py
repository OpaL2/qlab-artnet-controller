# -*- coding: utf-8 -*-

import asyncio

class DMX512Frame(object):

    def __init__(self, data = []):
        self._data = data + [0] * (512 - len(data))

    def get_data(self):
        return self._data

    def get_channel_value(self, ch):
        return self._data[ch - 1]

    def __call__(self, channel):
        return self._data[channel]

    def __eq__(self, other):
        return self._data == other._data

    def __ne__(self, other):
        return self._data != other._data

    def __iter__(self):
        self.__counter = 0
        return self

    def __next__(self):
        if self.__counter > 511:
            raise StopIteration
        else:
            self.__counter += 1
            return self.__counter - 1, self._data[self.__counter - 1]

    def __str__(self):
        return str(self._data)

class Universe(asyncio.Queue):

    def __init__(self, universe):
        super().__init__(maxsize=20)
        self._universe = universe

    def get_universe(self):
        return self._universe

    def create_callback_executor(self):
        return CallbackExecutor(self)

class CallbackExecutor(object):

    def __init__(self, universe):
        self._input = universe
        self._callbacks = {}
        self._previous = DMX512Frame()
        self._close = False

    def add_coroutine_callback(self, channel, callback):

        self._callbacks[channel - 1] = callback

    def add_callback(self, channel, callback):

        async def _executor_callback(ch, packet):
            callback(ch, packet)

        self.add_coroutine_callback(channel, _executor_callback)

        return self

    def close(self):
        self._close = True

    async def run(self):
        while True:

            packet = await self._input.get()

            if (self._close):
                break

            asyncio.ensure_future(self._process(packet))

    async def _process(self, packet):
        if (self._previous != packet):
            for channel, value in packet:
                if self._previous(channel) != value:
                    try:
                        asyncio.ensure_future(self._callbacks[channel](channel + 1, packet))
                    except KeyError:
                        pass

            self._previous = packet

        self._input.task_done()



