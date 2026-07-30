"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from core.models import Oyster, OysterLog

class Command(BaseCommand):
    help = "Sets up the required user access groups."

    def handle(self, *args, **options):
        # Output warning message
        self.stdout.write(self.style.WARNING("WARNING: This will permanently delete all pre-existing groups!"))

        # Ask for confirmation
        confirm = None
        while confirm not in ["y", "n"]:
            confirm = input("Are you sure you want to continue? [y/n]: ").lower()
        
        if confirm != "y":
            raise CommandError("Operation canceled.")

        # Delete all groups
        Group.objects.all().delete()

        # Add new groups

        # Students Group
        Group.objects.create(
            name = "Access Group: Students"
        )

        # Teachers Group
        User = get_user_model()
        user_content_type = ContentType.objects.get_for_model(User)
        user_permissions = Permission.objects.filter(content_type=user_content_type)
        user_view_permissions = user_permissions.filter(codename__startswith='view_')
        
        teachers = Group.objects.create(
            name = "Access Group: Teachers",
        )

        teachers.permissions.set(user_view_permissions)

        # Mentors Group
        log_content_type = ContentType.objects.get_for_model(OysterLog)
        log_permissions = Permission.objects.filter(content_type=log_content_type)

        oyster_content_type = ContentType.objects.get_for_model(Oyster)
        oyster_permissions = Permission.objects.filter(content_type=oyster_content_type)

        mentors = Group.objects.create(
            name = "Access Group: Mentors"
        )

        mentors.permissions.set(oyster_permissions)
        mentors.permissions.add(log_permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created groups.'))