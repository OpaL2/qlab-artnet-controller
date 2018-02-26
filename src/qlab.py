# -*- coding: utf-8 -*-

import asyncio
import worker


class QLab(object):

    def __init__(self, inp)

        self._commands = {}
        self._worker = QLabWorker(inp, config, self._commands)

    def __call__(self):
        self._worker()

    def close(self):
        self._worker.close()

class QLabWorker(worker.AbstractWorker):

    def __init__(self, inp, config, commands):
        super().__init__(inp)
        self._config = config
        self._commands = commands
        self.state = QLabState()

    async def process_next(self, item):

    def complete_callback(self, f):
        pass

