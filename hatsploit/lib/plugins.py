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

from hatsploit.core.db.importer import Importer
from hatsploit.lib.storage import LocalStorage


class Plugins:
    importer = Importer()
    local_storage = LocalStorage()

    def get_plugins(self):
        return self.local_storage.get("plugins")

    def get_loaded_plugins(self):
        return self.local_storage.get("loaded_plugins")

    def plugins_completer(self, text):
        plugins = self.get_plugins()
        matches = []

        if plugins:
            for database in plugins:
                for plugin in plugins[database]:
                    if plugin.startswith(text):
                        matches.append(plugin)

        return matches

    def loaded_plugins_completer(self, text):
        plugins = self.get_loaded_plugins()

        if plugins:
            return [plugin for plugin in plugins if plugin.startswith(text)]
        return []

    def check_exist(self, name):
        all_plugins = self.get_plugins()
        if all_plugins:
            for database in all_plugins:
                plugins = all_plugins[database]
                if name in plugins:
                    return True
        return False

    def check_loaded(self, name):
        loaded_plugins = self.get_loaded_plugins()
        if loaded_plugins:
            if name in loaded_plugins:
                return True
        return False

    def get_database(self, name):
        all_plugins = self.get_plugins()
        if all_plugins:
            for database in all_plugins:
                plugins = all_plugins[database]
                if name in plugins:
                    return database
        return None

    def import_plugin(self, database, plugin):
        loaded_plugins = {}
        plugins = self.get_plugins()[database][plugin]
        try:
            loaded_plugins[plugin] = self.importer.import_plugin(plugins['Path'])
        except Exception:
            return None
        return loaded_plugins

    def import_plugins(self, path):
        return self.importer.import_plugins(path)

    def add_plugin(self, database, plugin):
        plugins = self.get_plugins()[database][plugin]

        plugin_object = self.import_plugin(database, plugin)
        if plugin_object:
            if self.get_loaded_plugins():
                self.local_storage.update("loaded_plugins", plugin_object)
            else:
                self.local_storage.set("loaded_plugins", plugin_object)
            self.get_loaded_plugins()[plugin].load()
        else:
            raise RuntimeError(f"Failed to load plugin: {cowsay}!")

    def load_plugin(self, plugin):
        plugins_shorts = self.local_storage.get("plugin_shorts")

        if plugins_shorts:
            if plugin.isdigit():
                plugin_number = int(plugin)

                if plugin_number in plugins_shorts:
                    plugin = plugins_shorts[plugin_number]

        if not self.check_loaded(plugin):
            if self.check_exist(plugin):
                database = self.get_database(plugin)
                self.add_plugin(database, plugin)
            else:
                raise RuntimeError(f"Invalid plugin: {plugin}!")
        else:
            raise RuntimeWarning(f"Plugin is already loaded: {plugin}.")

    def unload_plugin(self, plugin):
        plugins_shorts = self.local_storage.get("plugin_shorts")

        if plugins_shorts:
            if plugin.isdigit():
                plugin_number = int(plugin)

                if plugin_number in plugins_shorts:
                    plugin = plugins_shorts[plugin_number]

        if self.check_loaded(plugin):
            self.local_storage.delete_element("loaded_plugins", plugin)
        else:
            raise RuntimeError(f"Plugin is not loaded: {plugin}!")
