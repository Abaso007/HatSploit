"""
MIT License

Copyright (c) 2020-2022 EntySec

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

from hatsploit.lib.jobs import Jobs
from hatsploit.lib.loot import Loot
from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.encoders import Encoders
from hatsploit.lib.sessions import Sessions

from hatsploit.core.cli.colors import Colors
from hatsploit.core.cli.tables import Tables


class Show:
    jobs = Jobs()
    loot = Loot()
    local_storage = LocalStorage()
    modules = Modules()
    payloads = Payloads()
    encoders = Encoders()
    sessions = Sessions()

    colors = Colors()
    tables = Tables()

    def show_custom_commands(self, handler):
        commands_data = {}
        headers = ("Command", "Description")
        commands = handler

        for command in sorted(commands):
            label = commands[command].details["Category"]
            commands_data[label] = []
        for command in sorted(commands):
            label = commands[command].details["Category"]
            commands_data[label].append(
                (command, commands[command].details["Description"])
            )
        for label in sorted(commands_data):
            self.tables.print_table(
                label.title() + " Commands", headers, *commands_data[label]
            )

    def show_interface_commands(self):
        if self.local_storage.get("commands"):
            self.show_custom_commands(self.local_storage.get("commands"))
        else:
            raise RuntimeWarning("No commands available.")

    def show_plugin_commands(self):
        for plugin in self.local_storage.get("loaded_plugins"):
            loaded_plugin = self.local_storage.get("loaded_plugins")[plugin]
            if hasattr(loaded_plugin, "commands"):
                commands_data = {}
                headers = ("Command", "Description")
                commands = loaded_plugin.commands
                for label in sorted(commands):
                    commands_data[label] = []
                    for command in sorted(commands[label]):
                        commands_data[label].append(
                            (command, commands[label][command]["Description"])
                        )
                for label in sorted(commands_data):
                    self.tables.print_table(
                        label.title() + " Commands", headers, *commands_data[label]
                    )

    def show_module_commands(self):
        current_module = self.modules.get_current_module()
        if hasattr(current_module, "commands"):
            commands_data = []
            headers = ("Command", "Description")
            commands = current_module.commands
            for command in sorted(commands):
                commands_data.append((command, commands[command]["Description"]))
            self.tables.print_table("Module Commands", headers, *commands_data)

    def show_all_commands(self):
        self.show_interface_commands()
        if self.modules.get_current_module():
            self.show_module_commands()
        if self.local_storage.get("loaded_plugins"):
            self.show_plugin_commands()

    def show_jobs(self):
        if self.local_storage.get("jobs"):
            jobs_data = []
            headers = ("ID", "Name", "Module")
            jobs = self.local_storage.get("jobs")
            for job_id in jobs:
                jobs_data.append((job_id, jobs[job_id]["Name"], jobs[job_id]["Module"]))
            self.tables.print_table("Active Jobs", headers, *jobs_data)
        else:
            raise RuntimeWarning("No running jobs available.")

    def show_loot(self):
        loots = self.loot.list_loot()
        if loots:
            headers = ("Loot", "Path", "Time")
            self.tables.print_table("Collected Loot", headers, *loots)
        else:
            raise RuntimeWarning("No loot collected yet.")

    def show_module_databases(self):
        if self.local_storage.get("connected_module_databases"):
            databases_data = []
            number = 0
            headers = ("Number", "Name", "Path")
            databases = self.local_storage.get("connected_module_databases")

            for name in databases:
                databases_data.append((number, name, databases[name]["Path"]))
                number += 1
            self.tables.print_table(
                "Connected Module Databases", headers, *databases_data
            )
        else:
            raise RuntimeWarning("No module databases connected.")

    def show_payload_databases(self):
        if self.local_storage.get("connected_payload_databases"):
            databases_data = []
            number = 0
            headers = ("Number", "Name", "Path")
            databases = self.local_storage.get("connected_payload_databases")

            for name in databases:
                databases_data.append((number, name, databases[name]["Path"]))
                number += 1
            self.tables.print_table(
                "Connected Payload Databases", headers, *databases_data
            )
        else:
            raise RuntimeWarning("No payload databases connected.")

    def show_encoder_databases(self):
        if self.local_storage.get("connected_encoder_databases"):
            databases_data = []
            number = 0
            headers = ("Number", "Name", "Path")
            databases = self.local_storage.get("connected_encoder_databases")

            for name in databases:
                databases_data.append((number, name, databases[name]["Path"]))
                number += 1
            self.tables.print_table(
                "Connected Encoder Databases", headers, *databases_data
            )
        else:
            raise RuntimeWarning("No encoder databases connected.")

    def show_plugin_databases(self):
        if self.local_storage.get("connected_plugin_databases"):
            databases_data = []
            number = 0
            headers = ("Number", "Name", "Path")
            databases = self.local_storage.get("connected_plugin_databases")

            for name in databases:
                databases_data.append((number, name, databases[name]["Path"]))
                number += 1
            self.tables.print_table(
                "Connected Plugin Databases", headers, *databases_data
            )
        else:
            raise RuntimeWarning("No plugin databases connected.")

    def show_plugins(self):
        all_plugins = self.local_storage.get("plugins")
        headers = ("Number", "Plugin", "Name")

        plugins_shorts = {}
        number = 0

        for database in sorted(all_plugins):
            plugins_data = []
            plugins = all_plugins[database]

            for plugin in sorted(plugins):
                plugins_data.append(
                    (number, plugins[plugin]["Plugin"], plugins[plugin]["Name"])
                )
                plugins_shorts.update({number: plugins[plugin]["Plugin"]})
                number += 1

            self.tables.print_table(f"Plugins ({database})", headers, *plugins_data)

        if plugins_shorts:
            self.local_storage.set("plugin_shorts", plugins_shorts)
        else:
            raise RuntimeWarning("No plugins available.")

    def show_encoders(self):
        all_encoders = self.local_storage.get("encoders")
        headers = ("Number", "Encoder", "Name")

        encoders_shorts = {}
        number = 0

        for database in sorted(all_encoders):
            encoders_data = []
            encoders = all_encoders[database]

            for encoder in sorted(encoders):
                encoders_data.append(
                    (number, encoders[encoder]["Encoder"], encoders[encoder]["Name"])
                )
                encoders_shorts.update({number: encoders[encoder]["Encoder"]})
                number += 1

            self.tables.print_table(f"Encoders ({database})", headers, *encoders_data)

        if encoders_shorts:
            self.local_storage.set("encoder_shorts", encoders_shorts)
        else:
            raise RuntimeWarning("No encoders available.")

    def show_modules(self, category=None):
        all_modules = self.local_storage.get("modules")
        headers = ("Number", "Category", "Module", "Rank", "Name")

        modules_shorts = {}
        number = 0

        for database in sorted(all_modules):
            modules_data = []
            modules = all_modules[database]

            for module in sorted(modules):
                if category:
                    if category == modules[module]["Category"]:
                        modules_data.append(
                            (
                                number,
                                modules[module]["Category"],
                                modules[module]["Module"],
                                modules[module]["Rank"],
                                modules[module]["Name"],
                            )
                        )
                        modules_shorts.update({number: modules[module]["Module"]})
                        number += 1
                else:
                    modules_data.append(
                        (
                            number,
                            modules[module]["Category"],
                            modules[module]["Module"],
                            modules[module]["Rank"],
                            modules[module]["Name"],
                        )
                    )
                    modules_shorts.update({number: modules[module]["Module"]})
                    number += 1

            if category:
                self.tables.print_table(
                    f"{category.title()} Modules ({database})", headers, *modules_data
                )
            else:
                self.tables.print_table(f"Modules ({database})", headers, *modules_data)

        if modules_shorts:
            self.local_storage.set("module_shorts", modules_shorts)
        else:
            raise RuntimeWarning("No modules available.")

    def show_payloads(self):
        all_payloads = self.local_storage.get("payloads")
        headers = ("Number", "Payload", "Rank", "Name")

        payloads_shorts = {}
        number = 0

        for database in sorted(all_payloads):
            payloads_data = []
            payloads = all_payloads[database]

            for payload in sorted(payloads):
                payloads_data.append(
                    (
                        number,
                        payloads[payload]["Payload"],
                        payloads[payload]["Rank"],
                        payloads[payload]["Name"],
                    )
                )
                payloads_shorts.update({number: payloads[payload]["Payload"]})
                number += 1

            self.tables.print_table(f"Payloads ({database})", headers, *payloads_data)

        if payloads_shorts:
            self.local_storage.set("payload_shorts", payloads_shorts)
        else:
            raise RuntimeWarning("No payloads available.")

    def show_search_plugins(self, keyword):
        all_plugins = self.local_storage.get("plugins")
        headers = ("Number", "Plugin", "Name")

        plugins_shorts = {}
        number = 0

        for database in all_plugins:
            plugins_data = []
            plugins = all_plugins[database]

            for plugin in sorted(plugins):
                if (
                    keyword in plugins[plugin]["Plugin"]
                    or keyword in plugins[plugin]["Name"]
                ):
                    name = plugins[plugin]["Plugin"].replace(
                        keyword, self.colors.RED + keyword + self.colors.END
                    )
                    description = plugins[plugin]["Name"].replace(
                        keyword, self.colors.RED + keyword + self.colors.END
                    )

                    plugins_data.append((number, name, description))
                    plugins_shorts.update({number: plugins[plugin]["Plugin"]})

                    number += 1

            if plugins_data:
                self.tables.print_table(f"Plugins ({database})", headers, *plugins_data)

        if plugins_shorts:
            self.local_storage.set("plugin_shorts", plugins_shorts)

    def show_search_encoders(self, keyword):
        all_encoders = self.local_storage.get("encoders")
        headers = ("Number", "Encoder", "Name")

        encoders_shorts = {}
        number = 0

        for database in all_encoders:
            encoders_data = []
            encoders = all_encoders[database]

            for encoder in sorted(encoders):
                if (
                    keyword in encoders[encoder]["Encoder"]
                    or keyword in encoders[encoder]["Name"]
                ):
                    name = encoders[encoder]["Encoder"].replace(
                        keyword, self.colors.RED + keyword + self.colors.END
                    )
                    description = encoders[encoder]["Name"].replace(
                        keyword, self.colors.RED + keyword + self.colors.END
                    )

                    encoders_data.append((number, name, description))
                    encoders_shorts.update({number: encoders[encoder]["Encoder"]})

                    number += 1

            if encoders_data:
                self.tables.print_table(
                    f"Encoders ({database})", headers, *encoders_data
                )

        if encoders_shorts:
            self.local_storage.set("encoder_shorts", encoders_shorts)

    def show_search_modules(self, keyword):
        all_modules = self.local_storage.get("modules")
        headers = ("Number", "Category", "Module", "Rank", "Name")

        modules_shorts = {}
        number = 0

        for database in all_modules:
            modules_data = []
            modules = all_modules[database]

            for module in sorted(modules):
                if (
                    keyword in modules[module]["Module"]
                    or keyword in modules[module]["Name"]
                ):
                    name = modules[module]["Module"].replace(
                        keyword, self.colors.RED + keyword + self.colors.END
                    )
                    description = modules[module]["Name"].replace(
                        keyword, self.colors.RED + keyword + self.colors.END
                    )

                    modules_data.append(
                        (
                            number,
                            modules[module]["Category"],
                            name,
                            modules[module]["Rank"],
                            description,
                        )
                    )
                    modules_shorts.update({number: modules[module]["Module"]})

                    number += 1

            if modules_data:
                self.tables.print_table(f"Modules ({database})", headers, *modules_data)

        if modules_shorts:
            self.local_storage.set("module_shorts", modules_shorts)

    def show_search_payloads(self, keyword):
        all_payloads = self.local_storage.get("payloads")
        headers = ("Number", "Payload", "Rank", "Name")

        payloads_shorts = {}
        number = 0

        for database in all_payloads:
            payloads_data = []
            payloads = all_payloads[database]

            for payload in sorted(payloads):
                if (
                    keyword in payloads[payload]["Payload"]
                    or keyword in payloads[payload]["Name"]
                ):
                    name = payloads[payload]["Payload"].replace(
                        keyword, self.colors.RED + keyword + self.colors.END
                    )
                    description = payloads[payload]["Name"].replace(
                        keyword, self.colors.RED + keyword + self.colors.END
                    )

                    payloads_data.append(
                        (number, name, payloads[payload]["Rank"], description)
                    )
                    payloads_shorts.update({number: payloads[payload]["Payload"]})

                    number += 1

            if payloads_data:
                self.tables.print_table(
                    f"Payloads ({database})", headers, *payloads_data
                )

        if payloads_shorts:
            self.local_storage.set("payload_shorts", payloads_shorts)

    def show_sessions(self):
        sessions = self.local_storage.get("sessions")
        if sessions:
            sessions_data = []
            headers = ("ID", "Platform", "Architecture", "Type", "Host", "Port")
            for session_id in sessions:
                session_platform = sessions[session_id]["Platform"]
                session_architecture = sessions[session_id]["Architecture"]
                session_type = sessions[session_id]["Type"]
                host = sessions[session_id]["Host"]
                port = sessions[session_id]["Port"]

                sessions_data.append(
                    (
                        session_id,
                        session_platform,
                        session_architecture,
                        session_type,
                        host,
                        port,
                    )
                )
            self.tables.print_table("Opened Sessions", headers, *sessions_data)
        else:
            raise RuntimeWarning("No opened sessions available.")

    def show_information(self, details):
        if "Name" in details:
            self.badges.print_information(f"Name: {details['Name']}")
        if "Module" in details:
            self.badges.print_information(f"Module: {details['Name']}")

    def show_options(self):
        current_module = self.modules.get_current_module()

        if not current_module:
            raise RuntimeWarning("No module selected.")

        if not hasattr(current_module, "options") and not hasattr(
            current_module, "payload"
        ):
            raise RuntimeWarning("Module has no options.")

        if not hasattr(current_module, "options") and not hasattr(
            self.payloads.get_current_payload(), "options"
        ):
            raise RuntimeWarning("Module has no options.")

        headers = ("Option", "Value", "Required", "Description")

        if hasattr(current_module, "options"):
            options_data = []
            options = current_module.options

            for option in sorted(options):
                value, required = options[option]["Value"], options[option]["Required"]
                if required:
                    required = "yes"
                else:
                    required = "no"
                if not value and value != 0:
                    value = ""
                options_data.append(
                    (option, value, required, options[option]["Description"])
                )
            self.tables.print_table(
                f"Module Options ({current_module.details['Module']})",
                headers,
                *options_data,
            )

        if hasattr(current_module, "payload"):
            current_payload = self.payloads.get_current_payload()
            current_encoder = self.encoders.get_current_encoder()

            if current_payload and hasattr(current_payload, "options"):
                options_data = []

                for option in sorted(current_payload.options):
                    value, required = (
                        current_payload.options[option]["Value"],
                        current_payload.options[option]["Required"],
                    )
                    if required:
                        required = "yes"
                    else:
                        required = "no"
                    if not value and value != 0:
                        value = ""
                    options_data.append(
                        (
                            option,
                            value,
                            required,
                            current_payload.options[option]["Description"],
                        )
                    )
                self.tables.print_table(
                    f"Payload Options ({current_payload.details['Payload']})",
                    headers,
                    *options_data,
                )

            if current_encoder and hasattr(current_encoder, "options"):
                options_data = []

                for option in sorted(current_encoder.options):
                    value, required = (
                        current_encoder.options[option]["Value"],
                        current_encoder.options[option]["Required"],
                    )
                    if required:
                        required = "yes"
                    else:
                        required = "no"
                    if not value and value != 0:
                        value = ""
                    options_data.append(
                        (
                            option,
                            value,
                            required,
                            current_encoder.options[option]["Description"],
                        )
                    )
                self.tables.print_table(
                    f"Encoder Options ({current_payload.details['Payload']})",
                    headers,
                    *options_data,
                )

    def show_advanced(self):
        current_module = self.modules.get_current_module()

        if not current_module:
            raise RuntimeWarning("No module selected.")

        if not hasattr(current_module, "advanced") and not hasattr(
            current_module, "payload"
        ):
            raise RuntimeWarning("Module has no advanced options.")

        if not hasattr(current_module, "advanced") and not hasattr(
            self.payloads.get_current_payload(), "advanced"
        ):
            raise RuntimeWarning("Module has no advanced options.")

        headers = ("Option", "Value", "Required", "Description")

        if hasattr(current_module, "advanced"):
            options_data = []
            options = current_module.advanced

            for option in sorted(options):
                value, required = options[option]["Value"], options[option]["Required"]
                if required:
                    required = "yes"
                else:
                    required = "no"
                if not value and value != 0:
                    value = ""
                options_data.append(
                    (option, value, required, options[option]["Description"])
                )
            self.tables.print_table(
                f"Module Advanced Options ({current_module.details['Module']})",
                headers,
                *options_data,
            )

        if hasattr(current_module, "payload"):
            current_payload = self.payloads.get_current_payload()
            current_encoder = self.encoders.get_current_encoder()

            if current_payload and hasattr(current_payload, "advanced"):
                options_data = []

                for option in sorted(current_payload.advanced):
                    value, required = (
                        current_payload.advanced[option]["Value"],
                        current_payload.advanced[option]["Required"],
                    )
                    if required:
                        required = "yes"
                    else:
                        required = "no"
                    if not value and value != 0:
                        value = ""
                    options_data.append(
                        (
                            option,
                            value,
                            required,
                            current_payload.advanced[option]["Description"],
                        )
                    )
                self.tables.print_table(
                    f"Payload Advanced Options ({current_payload.details['Payload']})",
                    headers,
                    *options_data,
                )

            if current_encoder and hasattr(current_encoder, "advanced"):
                options_data = []

                for option in sorted(current_encoder.advanced):
                    value, required = (
                        current_encoder.advanced[option]["Value"],
                        current_encoder.advanced[option]["Required"],
                    )
                    if required:
                        required = "yes"
                    else:
                        required = "no"
                    if not value and value != 0:
                        value = ""
                    options_data.append(
                        (
                            option,
                            value,
                            required,
                            current_encoder.advanced[option]["Description"],
                        )
                    )
                self.tables.print_table(
                    f"Encoder Advanced Options ({current_payload.details['Payload']})",
                    headers,
                    *options_data,
                )
