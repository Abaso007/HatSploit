"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.core.db.builder import Builder
from hatsploit.core.db.db import DB
from hatsploit.lib.command import Command
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.db = DB()
        self.builder = Builder()
        self.show = Show()

        self.details = {
            'Category': "databases",
            'Name': "payload_db",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer',
            ],
            'Description': "Manage payload databases.",
            'Usage': "payload_db <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                '-l': ['', "List all connected payload databases."],
                '-d': ['<name>', "Disconnect specified payload database."],
                '-c': ['<name> <path>', "Connect new payload database."],
                '-b': [
                    '<path> <output_path>',
                    "Build payload database from payloads path.",
                ],
            },
        }

    def run(self, argc, argv):
        choice = argv[1]

        if choice == '-b':
            self.builder.build_payload_database(argv[2], argv[3])
        elif choice == '-c':
            self.db.connect_payload_database(argv[2], argv[3])
        elif choice == '-d':
            self.db.disconnect_payload_database(argv[2])
        elif choice == '-l':
            self.show.show_payload_databases()
