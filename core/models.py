from django.db import models
from django.contrib.auth.models import AbstractUser, Group
import logging

logger = logging.getLogger(__name__)

# Create your models here.
class CustomUser(AbstractUser):
    @property
    def is_student(self) -> bool:
        "Is the user in the student group?"
        try:
            group = Group.objects.get(
                name = "Students"
            )

            return self.groups.contains(group)
        except Group.DoesNotExist:
            logging.warning("The students group does not exist. Run python manage.py setupgroups to create it.")
            return False

    @property
    def is_teacher(self) -> bool:
        "Is the user in the teacher group?"
        try:
            group = Group.objects.get(
                name = "Teachers"
            )

            return self.groups.contains(group)
        except Group.DoesNotExist:
            logging.warning("The teachers group does not exist. Run python manage.py setupgroups to create it.")
            return False

    @property
    def is_mentor(self) -> bool:
        "Is the user in the mentor group?"
        try:
            group = Group.objects.get(
                name = "Mentors"
            )

            return self.groups.contains(group)
        except Group.DoesNotExist:
            logging.warning("The mentors group does not exist. Run python manage.py setupgroups to create it.")
            return False