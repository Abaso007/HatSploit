"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.modules import Modules
from hatsploit.lib.runtime import Runtime
from hatsploit.lib.sessions import Sessions


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.modules = Modules()
        self.jobs = Jobs()
        self.runtime = Runtime()
        self.sessions = Sessions()

        self.details = {
            'Category': "modules",
            'Name': "run",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer',
            ],
            'Description': "Run current module.",
            'Usage': "run [option]",
            'MinArgs': 0,
            'Options': {'-j': ['', "Run current module as a background job."]},
        }

    def run(self, argc, argv):
        current_module = self.modules.get_current_module()

        if argc > 1:
            if argv[1] == '-j' and current_module:
                job_id = self.jobs.count_jobs()

                self.sessions.disable_auto_interaction() # so it won't break prompt

                self.print_process("Running module as a background job...")
                self.print_information(
                    f"Module started as a background job {str(job_id)}."
                )

                self.jobs.create_job(
                    current_module.details['Name'],
                    current_module.details['Module'],
                    self.runtime.catch,
                    [self.modules.run_current_module],
                )
                return

        self.modules.run_current_module()
