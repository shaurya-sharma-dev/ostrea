from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.db.models import Exists, OuterRef
import logging

# Register your models here.
User = get_user_model()

# Get logger
logger = logging.Logger(__name__)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom Admin for CustomUser model ensuring proper data privacy.
    """

    readonly_fields = ("date_joined", "last_login")
    
    def get_queryset(self, request):
        # Fetch default queryset.
        qs = super().get_queryset(request)
        
        # Superusers can always view users.
        if request.user.is_superuser:
            return qs
        
        is_teacher = request.user.is_teacher

        if not is_teacher:
            # If it is not a teacher, return an empty queryset.
            # The user must have been given permissions incorrectly.
            logger.warning("A user has view users permission without being a superuser or teacher. The system has not given them access to users.")
            return User.objects.none()

        admin_group_ids = request.user.groups.values_list('id', flat=True)

        student_group_membership = Group.objects.filter(
            name="Students",
            user=OuterRef("pk"),
        )
        
        return qs.annotate(
            is_student_group=Exists(student_group_membership)
        ).filter(
            is_student_group=True,              # Must be a student
            groups__id__in=admin_group_ids      # Shares a group with the teacher
        ).distinct() # distinct() prevents row duplicates if users share multiple groups