#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Name': "Windows Calculator",
        'Payload': "windows/cmd/calc",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Windows calc.exe payload.",
        'Architecture': "cmd",
        'Platform': "windows",
        'Rank': "high",
        'Type': "one_side"
    }

    def run(self):
        payload = "calc.exe"

        return payload
