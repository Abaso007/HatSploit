#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.com
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from pex.proto.http import HTTPClient
from pex.proto.tcp import TCPTools


class HatSploitModule(HTTPClient, Module, TCPTools):
    details = {
        'Category': 'auxiliary',
        'Name': 'HTTP Methods',
        'Module': 'auxiliary/generic/scanner/http_methods',
        'Authors': ['Noah Altunian (naltun) - contributor'],
        'Description': 'Find supported HTTP methods on a server',
        'Platform': 'generic',
        'Rank': 'low',
    }

    options = {
        'HOST': {
            'Description': 'Remote host.',
            'Value': None,
            'Type': 'ip',
            'Required': True,
        }
    }

    http_methods = [
        'CONNECT',
        'DELETE',
        'GET',
        'HEAD',
        'OPTIONS',
        'PATCH',
        'POST',
        'PUT',
        'TRACE',
    ]

    supported_methods = {'80': [], '443': []}

    def run(self):
        remote_host = self.parse_options(self.options)

        self.print_process(f'Scanning {remote_host}...')
        for port in [80, 443]:
            if self.check_tcp_port(remote_host, port):
                for method in self.http_methods:
                    resp = self.http_request(
                        method=method,
                        host=remote_host,
                        port=port,
                        path='/',
                    )

                    if resp:
                        if resp.status_code == 200:
                            self.supported_methods[str(port)].append(method)
        count = 0
        if len(self.supported_methods['80']):
            count += 1
            self.print_success(
                f'Port 80 Supported Methods: {" ".join(self.supported_methods["80"])}'
            )
        if len(self.supported_methods['443']):
            count += 1
            self.print_success(
                f'Port 443 Supported Methods: {" ".join(self.supported_methods["443"])}'
            )
        if count == 0:
            self.print_error('No supported HTTP methods detected')
