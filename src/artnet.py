# -*- coding: utf-8 -*-

import asyncio
import socket

from dmx512 import Universe, DMX512Frame

class ArtNet(asyncio.DatagramProtocol):
    #Contains ID, opcode and protocol version, rest is to be parsed
    ARTNET_HEADER = bytes([65,114,116,45,78,101,116,0,0,80,0,14])

    def __init__(self, loop, addr):
        self._loop = loop
        self._transport = None
        self._universes = {}
        self._sequence = 0


        listen = loop.create_datagram_endpoint(self, local_addr = addr)
        asyncio.ensure_future(listen)

    def connection_made(self, transport):
        self._transport = transport

    def create_universe(self, universe):
        u = Universe(universe)
        self._universes[universe] = u
        return u

    def datagram_received(self, data, addr):

        async def receive_cb(uni, frame):
            try:
                await self._universes[uni].put(frame)
            except KeyError:
                pass


        if(data[0:12] == self.ARTNET_HEADER):

            sequence = data[12]
            physical = data[13]
            universe = data[15] << 8 | data[14]
            length = data[16] << 8 | data[17]
            frame = DMX512Frame(list(data[18:]))

            #TODO: sequence check?
            asyncio.ensure_future(receive_cb(universe, frame))

    def __call__(self):
        return self

    def close(self):
        self._transport.close()
