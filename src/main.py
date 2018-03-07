#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import json
import ipaddress

import artnet

def load_config():
    with open('../config/config.json', 'r') as f:
        config = json.load(f)
        f.close()
        return config

def get_broadcast_address(config):
    return ipaddress.IPv4Network("%s/%s" % (config["networking"]["address"], config["networking"]["subnet"])).broadcast_address

def pretty_print(packet):
    print("Value change detected: %s" % channel)
    print("New value buffer: \n %s" % packet)

def get_callback(value):
  return value, pretty_print

config = load_config()

loop = asyncio.get_event_loop()
addr =(get_broadcast_address(config), config["networking"]["port"])
ArtNet = artnet.ArtNet(loop, addr)
worker = ArtNet.create_universe(0) \
    .create_callback_executor() \
    .add_callback(*get_callback(1)) \
    .add_callback(2, pretty_print)

asyncio.ensure_future(worker.run())

# Running loop, exiting on keyboard interrupt
try:
    loop.run_forever()
except KeyboardInterrupt:
    worker.close()
    ArtNet.close()
    loop.close()
    exit(0)
except Exception as e:
    print("Encountered error: %s, exiting..." % e)
    worker.close()
    ArtNet.close()
    loop.close()
    exit(1)