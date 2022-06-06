"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    show = Show()

    details = {
        'Category': "encoder",
        'Name': "encoders",
        'Authors': ['Ivan Nikolsky (enty8080) - command developer'],
        'Description': "Show available encoders.",
        'Usage': "encoders",
        'MinArgs': 0,
    }

    def run(self, argc, argv):
        self.show.show_encoders()
