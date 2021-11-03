#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.core.base.execute import Execute
from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    execute = Execute()

    details = {
        'Category': "developer",
        'Name': "exec",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Execute local system command.",
        'Usage': "exec <command>",
        'MinArgs': 1
    }

    def run(self, argc, argv):
        command = self.format_commands(argv[1])
        self.execute.execute_system(command)
