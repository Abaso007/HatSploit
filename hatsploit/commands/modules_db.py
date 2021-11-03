#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.core.db.builder import Builder
from hatsploit.core.db.db import DB
from hatsploit.lib.command import Command
from hatsploit.lib.storage import LocalStorage


class HatSploitCommand(Command):
    db = DB()
    builder = Builder()
    local_storage = LocalStorage()

    usage = ""
    usage += "module_db <option> [arguments]\n\n"
    usage += "  -l, --list                        List all connected module databases.\n"
    usage += "  -d, --disconnect <name>           Disconnect specified module database.\n"
    usage += "  -c, --connect <name> <path>       Connect new module database.\n"
    usage += "  -b, --build <path> <output_path>  Build module database from modules path.\n"

    details = {
        'Category': "databases",
        'Name': "module_db",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage module databases.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        choice = argv[1]
        if choice in ['-l', '--list']:
            if self.local_storage.get("connected_modules_databases"):
                databases_data = list()
                number = 0
                headers = ("Number", "Name", "Path")
                databases = self.local_storage.get("connected_modules_databases")
                for name in databases.keys():
                    databases_data.append((number, name, databases[name]['path']))
                    number += 1
                self.print_table("Connected Module Databases", headers, *databases_data)
            else:
                self.print_warning("No module database connected.")
        elif choice in ['-d', '--disconnect']:
            if argc < 3:
                self.print_usage(self.details['Usage'])
            else:
                self.db.disconnect_modules_database(argv[2])
        elif choice in ['-b', '--build']:
            if argc < 4:
                self.print_usage(self.details['Usage'])
            else:
                self.builder.build_modules_database(argv[2], argv[3])
        elif choice in ['-c', '--connect']:
            if argc < 4:
                self.print_usage(self.details['Usage'])
            else:
                self.db.connect_modules_database(argv[2], argv[3])
        else:
            self.print_usage(self.details['Usage'])
