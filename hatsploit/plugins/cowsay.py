"""
This plugin requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import textwrap

from hatsploit.lib.plugin import Plugin


class HatSploitPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.details = {
            'Name': "HatSploit Cowsay Implementation",
            'Plugin': "cowsay",
            'Authors': [
                'Ivan Nikolsky (enty8080) - plugin developer',
            ],
            'Description': "Cowsay plugin for HatSploit.",
        }

        self.commands = {
            'cowsay': {
                'cowsay': {
                    'Description': "Ask cow to say message.",
                    'Usage': "cowsay <message>",
                    'MinArgs': 1,
                }
            }
        }

    def ask_cow(self, message, length=40):
        return self.build_bubble(message, length) + self.build_cow()

    @staticmethod
    def get_border(lines, index):
        if len(lines) < 2:
            return ["<", ">"]
        if index == 0:
            return ["/", "\\"]
        return ["\\", "/"] if index == len(lines) - 1 else ["|", "|"]

    @staticmethod
    def build_cow():
        return """
         \   ^__^ 
          \  (oo)\_______
             (__)\       )\/\\
                 ||----w |
                 ||     ||
        """

    @staticmethod
    def normalize_text(message, length):
        lines = textwrap.wrap(message, length)
        maxlen = len(max(lines, key=len))
        return [line.ljust(maxlen) for line in lines]

    def build_bubble(self, message, length=40):
        lines = self.normalize_text(message, length)
        bordersize = len(lines[0])
        bubble = [" __" + "_" * bordersize]
        for index, line in enumerate(lines):
            border = self.get_border(lines, index)
            bubble.append(f"{border[0]} {line} {border[1]}")
        bubble.append(" --" + "-" * bordersize)
        return "\n".join(bubble)

    def cowsay(self, _, argv):
        message = argv[1]
        cow = self.ask_cow(message, len(message))
        self.print_empty(cow)

    def load(self):
        message = "Cow here, moo!"
        cow = self.ask_cow(message, len(message))
        self.print_empty(cow)

        self.print_information("Use %greencowsay%end to call me.")
