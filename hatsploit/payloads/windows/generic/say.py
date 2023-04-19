"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details = {
            'Name': "Windows Say",
            'Payload': "windows/generic/say",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Say payload for Windows.",
            'Architecture': "generic",
            'Platform': "windows",
            'Rank': "low",
            'Type': "one_side",
        }

        self.options = {
            'MESSAGE': {
                'Description': "Message to say.",
                'Value': "Hello, Friend!",
                'Type': None,
                'Required': True,
            }
        }

    def run(self):
        message = self.parse_options(self.options)

        source = (
            "Add-Type -AssemblyName System.speech;"
            "$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;"
            f"$speak.Speak('{message}')"
        )

        return f"powershell -w hidden -nop -c {source}"
