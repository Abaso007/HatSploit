"""
MIT License

Copyright (c) 2020-2023 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import os

from hatsploit.core.cli.badges import Badges
from hatsploit.core.db.importer import Importer
from hatsploit.lib.config import Config
from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.storage import LocalStorage


class Builder(object):
    def __init__(self):
        super().__init__()

        self.modules = Modules()
        self.payloads = Payloads()
        self.badges = Badges()
        self.config = Config()
        self.importer = Importer()
        self.local_storage = LocalStorage()

    def check_base_built(self):
        if (
                os.path.exists(
                    self.config.path_config['db_path']
                    + self.config.db_config['base_dbs']['module_database']
                )
                and os.path.exists(
            self.config.path_config['db_path'] + self.config.db_config['base_dbs']['payload_database'])
                and os.path.exists(
            self.config.path_config['db_path']
            + self.config.db_config['base_dbs']['plugin_database']
        )
                and os.path.exists(
            self.config.path_config['db_path']
            + self.config.db_config['base_dbs']['encoder_database']
        )
        ):
            return True
        return False

    def rebuild_base(self):
        if self.check_base_build():
            self.build_base()
            return True
        return False

    def build_base(self):
        if not os.path.exists(self.config.path_config['db_path']):
            os.mkdir(self.config.path_config['db_path'])

        self.build_module_database(
            self.config.path_config['modules_path'],
            (
                    self.config.path_config['db_path']
                    + self.config.db_config['base_dbs']['module_database']
            ),
        )
        self.build_payload_database(
            self.config.path_config['payloads_path'],
            (
                    self.config.path_config['db_path']
                    + self.config.db_config['base_dbs']['payload_database']
            ),
        )
        self.build_encoder_database(
            self.config.path_config['encoders_path'],
            (
                    self.config.path_config['db_path']
                    + self.config.db_config['base_dbs']['encoder_database']
            ),
        )
        self.build_plugin_database(
            self.config.path_config['plugins_path'],
            (
                    self.config.path_config['db_path']
                    + self.config.db_config['base_dbs']['plugin_database']
            ),
        )

    def build_encoder_database(self, input_path, output_path):
        database_path = output_path
        database = {"__database__": {"Type": "encoders"}}

        encoders_path = os.path.normpath(input_path)
        for dest, _, files in os.walk(encoders_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    encoder = dest + '/' + file[:-3]

                    try:
                        encoder_object = self.importer.import_encoder(encoder)
                        encoder_name = encoder_object.details['Encoder']

                        database.update(
                            {
                                encoder_name: {
                                    "Path": encoder,
                                    "Name": encoder_object.details['Name'],
                                    "Encoder": encoder_object.details['Encoder'],
                                    "Authors": encoder_object.details['Authors'],
                                    "Desctiption": encoder_object.details[
                                        'Description'
                                    ],
                                    "Architecture": encoder_object.details[
                                        'Architecture'
                                    ],
                                }
                            }
                        )
                    except Exception:
                        self.badges.print_error(
                            f"Failed to add {encoder} to encoder database!"
                        )

        with open(database_path, 'w') as f:
            json.dump(database, f)

    def build_payload_database(self, input_path, output_path):
        database_path = output_path
        database = {"__database__": {"Type": "payloads"}}

        payloads_path = os.path.normpath(input_path)
        for dest, _, files in os.walk(payloads_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    payload = dest + '/' + file[:-3]

                    try:
                        payload_object = self.importer.import_payload(payload)
                        payload_name = payload_object.details['Payload']

                        database.update(
                            {
                                payload_name: {
                                    "Path": payload,
                                    "Name": payload_object.details['Name'],
                                    "Payload": payload_object.details['Payload'],
                                    "Authors": payload_object.details['Authors'],
                                    "Description": payload_object.details[
                                        'Description'
                                    ],
                                    "Architecture": payload_object.details[
                                        'Architecture'
                                    ],
                                    "Platform": payload_object.details['Platform'],
                                    "Rank": payload_object.details['Rank'],
                                    "Type": payload_object.details['Type'],
                                }
                            }
                        )
                    except Exception:
                        self.badges.print_error(
                            f"Failed to add {payload} to payload database!"
                        )

        with open(database_path, 'w') as f:
            json.dump(database, f)

    def build_module_database(self, input_path, output_path):
        database_path = output_path
        database = {"__database__": {"Type": "modules"}}

        modules_path = os.path.normpath(input_path)
        for dest, _, files in os.walk(modules_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    module = dest + '/' + file[:-3]

                    try:
                        module_object = self.importer.import_module(module)
                        module_name = module_object.details['Module']

                        database.update(
                            {
                                module_name: {
                                    "Path": module,
                                    "Category": module_object.details['Category'],
                                    "Name": module_object.details['Name'],
                                    "Module": module_object.details['Module'],
                                    "Authors": module_object.details['Authors'],
                                    "Description": module_object.details['Description'],
                                    "Platform": module_object.details['Platform'],
                                    "Rank": module_object.details['Rank'],
                                }
                            }
                        )
                    except Exception:
                        self.badges.print_error(
                            f"Failed to add {module} to module database!"
                        )

        with open(database_path, 'w') as f:
            json.dump(database, f)

    def build_plugin_database(self, input_path, output_path):
        database_path = output_path
        database = {"__database__": {"Type": "plugins"}}

        plugins_path = os.path.normpath(input_path)
        for dest, _, files in os.walk(plugins_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    plugin = dest + '/' + file[:-3]

                    try:
                        plugin_object = self.importer.import_plugin(plugin)
                        plugin_name = plugin_object.details['Plugin']

                        database.update(
                            {
                                plugin_name: {
                                    "Path": plugin,
                                    "Name": plugin_object.details['Name'],
                                    "Plugin": plugin_object.details['Plugin'],
                                    "Authors": plugin_object.details['Authors'],
                                    "Description": plugin_object.details['Description'],
                                }
                            }
                        )
                    except Exception:
                        self.badges.print_error(
                            f"Failed to add {plugin} to plugin database!"
                        )

        with open(database_path, 'w') as f:
            json.dump(database, f)
