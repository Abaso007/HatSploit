"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    jobs = Jobs()
    show = Show()

    details = {
        'Category': "jobs",
        'Name': "jobs",
        'Authors': ['Ivan Nikolsky (enty8080) - command developer'],
        'Description': "Manage active jobs.",
        'Usage': "jobs <option> [arguments]",
        'MinArgs': 1,
        'Options': {
            '-l': ['', 'List all active jobs.'],
            '-k': ['<id>', 'Kill specified job.'],
        },
    }

    def run(self, argc, argv):
        choice = argv[1]

        if choice == '-l':
            self.show.show_jobs()

        elif choice == '-k':
            self.jobs.delete_job(argv[2])
