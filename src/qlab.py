# -*- coding: utf-8 -*-

import asyncio
import json
import os

class QLab(object):

    def __init__(self, control_channel, parameter_channel):
        self._control_channel = control_channel
        self._parameter_channel = parameter_channel
        self._executors = {}

    def parse_executors(self, applescript_path):
        path = os.path.abspath(applescript_path) + '/'
        with open(path + 'commands.json', 'r') as f:
            config = json.load(f)
            f.close()
            for item in config["commands"]:
                self._add_executor(item["channel_value"], Executor(item['takes_parameter'], path + item['script_name']))
        return self

    def get_callback(self):
        return self._control_channel, self._callback

    def _add_executor(self, channel_value, executor):
        self._executors[channel_value] = executor

    async def _callback(self, packet):
        try:
            executor = self._executors[packet.get_channel_value(self._control_channel)]
            print("Executing script: %s" % executor)
            process = await asyncio.create_subprocess_exec(executor(packet.get_channel_value(self._parameter_channel)))

            await process.wait()
            returncode = process.returncode
            if returncode != 0:
                raise Exception("Script %s errored" % executor)

        except KeyError:
            pass
        except FileNotFoundError:
            print("Script file not found %s" % executor)

class Executor(object):

    def __init__(self, has_params, script_path):
        self._has_params = has_params
        self._script_path = script_path

    def __call__(self, param = 0):
        if self._has_params:
            return ' '.join(["osascript", self._script_path, str(param)])
        else:
            return ["osascript", self._script_path]

    def __str__(self):
        return self._script_path