#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import json
import ipaddress
import os
import sys

import artnet
import qlab

def load_config(working_dir):
    with open(working_dir + '/../config/config.json', 'r') as f:
        config = json.load(f)
        f.close()
        return config

def get_broadcast_address(config):
    return str(ipaddress.ip_interface("%s/%s" % (config["networking"]["address"], config["networking"]["subnet"])).network.broadcast_address)

def pretty_print(packet):
    print("Value change detected" )
    print("New value buffer: \n %s" % packet)

working_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
config = load_config(working_dir)

qlab = qlab.QLab(config["DMX512"]["control_channel"], config["DMX512"]["parameter_channel"]) \
    .parse_executors(working_dir + '/../src/applescript')

loop = asyncio.get_event_loop()
addr = (get_broadcast_address(config), config["networking"]["port"])

ArtNet = artnet.ArtNet(loop, addr)
worker = ArtNet.create_universe(config["DMX512"]["universe"]) \
    .create_callback_executor() \
    .add_coroutine_callback(*qlab.get_callback())

asyncio.ensure_future(worker.run())

# Running loop, exiting on keyboard interrupt
try:
    loop.run_forever()
except KeyboardInterrupt:
    worker.close()
    ArtNet.close()
    loop.close()
    exit(0)
