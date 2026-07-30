"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from django.core.management.base import BaseCommand, CommandError
from core.tests import set_up_test_data

class Command(BaseCommand):
    help = "Sets up the test data for development."

    def add_arguments(self, parser):
        parser.add_argument("password", type=str, help="The password to set for every user created.")

    def handle(self, *args, **options):
        # Output warning message
        self.stdout.write(self.style.WARNING("WARNING: This will permanently wipe the database!"))

        # Ask for confirmation
        confirm = None
        while confirm not in ["y", "n"]:
            confirm = input("Are you sure you want to continue? [y/n]: ").lower()
        
        if confirm != "y":
            raise CommandError("Operation canceled.")

        set_up_test_data(options["password"])

        self.stdout.write(self.style.SUCCESS('Setup test data successfully.'))