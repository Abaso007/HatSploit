#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.com
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.encoder import Encoder
from pex.string import String


class HatSploitEncoder(Encoder, String):
    details = {
        'Name': "Base64 Encoder for Command",
        'Encoder': "generic/base64",
        'Authors': ['Ivan Nikolsky (enty8080) - payload developer'],
        'Description': "Encode command with base64.",
        'Architecture': "generic",
    }

    options = {
        'SHELL': {
            'Description': "Shell to execute.",
            'Value': "$SHELL",
            'Type': None,
            'Required': True,
        }
    }

    def run(self):
        shell = self.parse_options(self.options)

        encoded_payload = self.base64_string(self.payload)
        return f'base64 --decode <<< {encoded_payload} | {shell}'
