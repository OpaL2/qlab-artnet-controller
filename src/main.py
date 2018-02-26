#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import artnet
import worker

class Printer(worker.AbstractWorker):

    def __init__(self, inp):
        self._input = inp
        self._close = False

    def complete_callback(self, f):
        pass

    async def process_next(self, item):
        print(item.get_channel_value(1))

loop = asyncio.get_event_loop()
addr =('10.52.84.255', 0x1936)
ArtNet = artnet.ArtNet(loop, addr)
universe = ArtNet.create_universe(0)
printer = Printer(universe)

printer()


# Running loop, exiting on keyboard interrupt
try:
    loop.run_forever()
except KeyboardInterrupt:
    printer.close()
    ArtNet.close()
    loop.close()
    exit()