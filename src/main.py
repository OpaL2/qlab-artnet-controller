#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import artnet

def pretty_print(channel, packet):
    print("Value change detected: %s" % channel)
    print("New value buffer: \n %s" % packet)

loop = asyncio.get_event_loop()
addr =('10.100.63.255', 0x1936)
ArtNet = artnet.ArtNet(loop, addr)
universe = ArtNet.create_universe(0)
printer = universe.create_callback_executor() \
    .add_callback(0, pretty_print) \
    .add_callback(1, pretty_print)

asyncio.ensure_future(printer.run())

# Running loop, exiting on keyboard interrupt
try:
    loop.run_forever()
except KeyboardInterrupt:
    printer.close()
    ArtNet.close()
    loop.close()
    exit()