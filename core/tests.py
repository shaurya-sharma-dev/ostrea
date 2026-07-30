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
from .admin import CustomUserAdmin

# User model
User = get_user_model()

# Create your tests here.
def set_up_access_groups() -> dict[str, Group]:
    # Delete all groups
    Group.objects.all().delete()

    # Add new groups

    # Students Group
    students = Group.objects.create(
        name = "Access Group: Students"
    )

    # Teachers Group
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
    mentors.permissions.add(*log_permissions)

    return {
        "students": students,
        "teachers": teachers,
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

    # Create two school groups
    school1 = Group.objects.create(
        name = "School: Test 1",
    )

    school2 = Group.objects.create(
        name = "School: Test 2",
    )

    # Create two teachers with the corresponding school groups.
    teacher1 = User.objects.create_user(
        username="teacher1",
        email=None,
        password=password,
        is_staff=True,
    )

    teacher1.groups.add(school1)
    teacher1.groups.add(access_groups["teachers"])

    teacher2 = User.objects.create_user(
        username="teacher2",
        email=None,
        password=password,
        is_staff=True,
    )

    teacher2.groups.add(school2)
    teacher2.groups.add(access_groups["teachers"])

    # Create two students with the corresponding school groups.
    student1 = User.objects.create_user(
        username="student1",
        email=None,
        password=password,
    )

    student1.groups.add(school1)
    student1.groups.add(access_groups["students"])

    student2 = User.objects.create_user(
        username="student2",
        email=None,
        password=password,
    )

    student2.groups.add(school2)
    student2.groups.add(access_groups["students"])

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

    # Create two logs.
    log1 = OysterLog.objects.create(
        oyster=oyster1,
        ph_level=Decimal("5.0"),
    )

    log2 = OysterLog.objects.create(
        oyster=oyster2,
        ph_level=Decimal("5.0"),
    )

    return {
        "access_groups": access_groups,
        "schools": (school1, school2),
        "teachers": (teacher1, teacher2),
        "students": (student1, student2),
        "mentors": (mentor1, mentor2),
        "oysters": (oyster1, oyster2),
        "logs": (log1, log2),
        "superuser": superuser
    }