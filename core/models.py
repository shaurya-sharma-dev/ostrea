"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, Group
import logging
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.formats import date_format

logger = logging.getLogger(__name__)

# Create your models here.
class CustomUser(AbstractUser):
    @property
    def is_mentor(self) -> bool:
        "Is the user in the mentor group?"
        try:
            group = Group.objects.get(
                name = "Access Group: Mentors"
            )

            return self.groups.contains(group)
        except Group.DoesNotExist:
            logger.warning("The mentors group does not exist. Run python manage.py setupgroups to create it.")
            return False

    @property
    def display_name(self) -> str:
        short_name = self.get_short_name()
        if short_name:
            return short_name

        return self.username

class Oyster(models.Model):
    mentor = models.ForeignKey(
        to=CustomUser, 
        on_delete=models.CASCADE,
        help_text="The mentor that is growing the oyster.",
    )

    name = models.CharField(
        max_length=100,
        help_text="The \"name\" or ID of the oyster. You will use this to select oysters for logging.",
    )

    site_name = models.CharField(
        max_length=250,
        help_text="The name of the site (e.g. Lynnhaven River)"
    )

    site_location = models.CharField(
        max_length=250,
        help_text="The precise location of the site (e.g. Pleasure House Point)"
    )

    deployment_date = models.DateField(
        default=timezone.now,
        help_text="The date the cage/float was deployed into the water."
    )

    notes = models.TextField(
        max_length=500,
        help_text="Extra notes about the oyster (if desired)",
        blank=True, default=""
    )

    def __str__(self):
        return self.name

class OysterLog(models.Model):
    class Meta:
        verbose_name = "Oyster Log"
        verbose_name_plural = "Oyster Logs"

    oyster = models.ForeignKey(
        to=Oyster, 
        on_delete=models.CASCADE,
        help_text="The oyster to log."
    )

    date = models.DateField(
        default=timezone.now,
        help_text="The date of the log."
    )

    ph_level = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(14.0)
        ],
        help_text="The pH level of the water (0.00 - 14.00)"
    )

    field_logs = models.TextField(
        max_length=500,
        help_text="Extra notes for this log (if desired)",
        blank=True, default=""
    )

    def __str__(self):
        return f"Log for {self.oyster} on {date_format(self.date, "F jS, Y")}"