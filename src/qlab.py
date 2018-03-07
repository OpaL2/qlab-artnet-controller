# -*- coding: utf-8 -*-

import asyncio

class QLab(object):

    def __init__(self, control_channel, parameter_channel):
        self._control_channel = control_channel
        self._parameter_channel = parameter_channel
        self._executors = {}

    def parse_executors(self, executor_config):


    def get_callback(self):
        return self._control_channel, self._callback

    def _add_executor(self, channel_value, executor):
        self._executors[channel_value] = executor

    async def _callback(self, packet):
        try:
            executor = self._executors[packet.get_channel_value(self._control_channel)]
            process = await asyncio.create_subprocess_exec(executor(packet.get_channel_value(self._parameter_channel)))

            await process.wait()
            returncode = process.returncode
            if returncode != 0:
                raise Exception("Subprocess errored")

        except KeyError:
            pass


class Executor(object):

    def __init__(self, has_params, script_path):
        self._has_params = has_params
        self._script_path = script_path

    def __call__(self, param = 0):
        if self._has_params:
            return ["osascript", self._script_path, str(param)]
        else:
            return ["osascript", self._script_path]