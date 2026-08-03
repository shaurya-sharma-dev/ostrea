"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from core.models import Oyster, OysterLog
from django.contrib.admin.models import LogEntry
from decimal import Decimal
from django.contrib.admin.sites import AdminSite
from datetime import date
from .admin import OysterAdmin, OysterLogAdmin

# User model
User = get_user_model()

# Create your tests here.
def set_up_access_groups() -> dict[str, Group]:
    # Delete all groups
    Group.objects.all().delete()

    # Add new groups

    # Mentors Group
    log_content_type = ContentType.objects.get_for_model(OysterLog)
    log_permissions = Permission.objects.filter(content_type=log_content_type)

    oyster_content_type = ContentType.objects.get_for_model(Oyster)
    oyster_permissions = Permission.objects.filter(content_type=oyster_content_type)

    mentors = Group.objects.create(
        name = "Access Group: Mentors"
    )

    mentors.permissions.set(oyster_permissions)
    mentors.permissions.add(*log_permissions)

    return {
        "mentors": mentors,
    }

def set_up_test_data(password: str):
    # Wipe admin logs
    LogEntry.objects.all().delete()

    # Set up the access groups.
    access_groups = set_up_access_groups()

    # Wipe users
    User.objects.all().delete()

    # Create a superuser
    superuser = User.objects.create_superuser(
        username="admin",
        email=None,
        password=password
    )

    # Create two mentors.
    mentor1 = User.objects.create_user(
        username="mentor1",
        email=None,
        password=password,
        is_staff=True,
    )

    mentor1.groups.add(access_groups["mentors"])

    mentor2 = User.objects.create_user(
        username="mentor2",
        email=None,
        password=password,
        is_staff=True,
    )

    mentor2.groups.add(access_groups["mentors"])

    # Create two oysters.
    oyster1 = Oyster.objects.create(
        mentor=mentor1,
        name="oyster1",
        site_name="oyster1 site",
        site_location="oyster1 site location",
    )

    oyster2 = Oyster.objects.create(
        mentor=mentor2,
        name="oyster2",
        site_name="oyster2 site",
        site_location="oyster2 site location",
    )

    # Create two logs for each oyster.
    log1_1 = OysterLog.objects.create(
        oyster=oyster1,
        ph_level=Decimal("6.5"),
        date=date(2026, 1, 1),
    )

    log1_2 = OysterLog.objects.create(
        oyster=oyster1,
        ph_level=Decimal("7.3"),
        date=date(2026, 1, 8),
    )

    log2_1 = OysterLog.objects.create(
        oyster=oyster2,
        ph_level=Decimal("5.2"),
        date=date(2026, 1, 1),
    )

    log2_2 = OysterLog.objects.create(
        oyster=oyster2,
        ph_level=Decimal("9.3"),
        date=date(2026, 1, 8),
    )

    return {
        "access_groups": access_groups,
        "mentors": (mentor1, mentor2),
        "oysters": (oyster1, oyster2),
        "logs": ((log1_1, log1_2), (log2_1, log2_2)),
        "superuser": superuser
    }

class TestOysterAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = set_up_test_data(" ")
        cls.factory = RequestFactory()

    def setUp(self):
        self.model_admin = OysterAdmin(Oyster, AdminSite())

    def test_mentors_can_only_see_their_oysters(self):
        for index in range(2):
            with self.subTest(index=index):
                mentor = self.data["mentors"][index]
                request = self.factory.get("")
                request.user = mentor

                qs = self.model_admin.get_queryset(request)

                self.assertIn(self.data["oysters"][index], qs)

                self.assertNotIn(self.data["oysters"][(index + 1) % 2], qs)

                # The queryset should have just the oyster.
                self.assertEqual(qs.count(), 1, "Queryset has more than one oyster.")

    def test_superuser_can_see_all_oysters(self):
        request = self.factory.get("")
        request.user = self.data["superuser"]

        qs = self.model_admin.get_queryset(request)

        self.assertEqual(qs.count(), Oyster.objects.count(), "Superuser cannot see all oysters.")

class TestOysterLogAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = set_up_test_data(" ")
        cls.factory = RequestFactory()

    def setUp(self):
        self.model_admin = OysterLogAdmin(OysterLog, AdminSite())

    def test_mentors_can_only_see_their_logs(self):
        for index in range(2):
            with self.subTest(index=index):
                mentor = self.data["mentors"][index]
                request = self.factory.get("")
                request.user = mentor

                qs = self.model_admin.get_queryset(request)

                for log_index in range(2):
                    self.assertIn(self.data["logs"][index][log_index], qs)
                    self.assertNotIn(self.data["logs"][(index + 1) % 2][log_index], qs)

                # The queryset should have just the two logs.
                self.assertEqual(qs.count(), 2, "Queryset has more than two logs.")

    def test_superuser_can_see_all_logs(self):
        request = self.factory.get("")
        request.user = self.data["superuser"]

        qs = self.model_admin.get_queryset(request)

        self.assertEqual(qs.count(), OysterLog.objects.count(), "Superuser cannot see all logs.")