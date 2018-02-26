# -*- coding: utf-8 -*-

import asyncio

class ArtNet(asyncio.DatagramProtocol):
    #Contains ID, opcode and protocol version, rest is to be parsed
    ARTNET_HEADER = bytes([65,114,116,45,78,101,116,0,0,80,0,14])

    def __init__(self):
        self._transport = None
        self._universeQueues = {}
        self._sequence = 0

    def connection_made(self, transport):
        self._transport = transport

    def register_uni(self, uni, queue)
        self._universeQueues[uni] = queue

    def datagram_received(self, data, addr):

        async def receive_cb(uni, frame):
            try:
                await self._universeQueues[uni].put(frame)
            except KeyError:
                pass


        if(data[0:12] == ARTNET_HEADER):

            sequence = data[12]
            physical = data[13]
            universe = data[15] << 8 | data[14]
            length = data[16] << 8 | data[17]
            frame = DMX512Frame(list(data[18:]))

            #TODO: sequence check?
            asyncio.ensure_future(cb(universe, frame))

class DMX512Frame(object):

    def __init__(self, data):
        self._data = data + [0] * (512 - len(data))

    def get_data(self):
        return self._data

    def get_channel_value(self, ch):
        return self._data[ch - 1]