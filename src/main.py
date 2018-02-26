#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import artnet


loop = asyncio.get_event_loop()
Uni1 = asyncio.Queue(maxsize=20)
ArtNet = artnet.ArtNet().register_uni(0, Uni1)

listen = loop.create_datagram_endpoint(
    ArtNet,
    local_addr=('10.52.84.255', 0x1936)
    )

transport, proto = loop.run_until_complete(listen)

asyncio.ensure_future(printer(Uni1))


# Running loop, exiting on keyboard interrupt
try:
    loop.run_forever()
except KeyboardInterrupt:
    transport.close()
    loop.close()
    exit()