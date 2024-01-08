"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Category': "core",
            'Name': "clear",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Clear terminal window.",
            'Usage': "clear",
            'MinArgs': 0,
        })

    def run(self, argc, argv):
        self.print_empty("%clear", end='')
