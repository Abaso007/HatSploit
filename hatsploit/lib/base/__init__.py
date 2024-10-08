"""
MIT License

Copyright (c) 2020-2024 EntySec

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

from hatasm import HatAsm

from badges import Badges, Tables


class BaseMixin(Badges, Tables):
    """ Subclass of hatsploit.lib.base module.

    This subclass of hatsploit.lib.base module is a representation
    of a parent class for all modules, payloads, commands, plugins,
    encoders, sessions, etc.
    """

    def __init__(self, info: dict) -> None:
        """ Initialize base module.

        :param dict info: context information (e.g. module details)
        :return None: None
        """

        self.info = info

    def __asm__(self, code: str, *args, **kwargs) -> bytes:
        """ Assemble assembly code using current architecture.

        :param str code: assembly code
        :return bytes: assembled code
        """

        return HatAsm().assemble(self.info['Arch'], code, *args, **kwargs)
