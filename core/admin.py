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

# GroupFilter class
class GroupFilter(admin.SimpleListFilter):
    """
    Custom SimpleListFilter to protect groups teachers aren't in from being exposed.
    """
    
    title = "groups"
    parameter_name = "groups"

    def lookups(self, request, model_admin):
        """
        Define the filter choices visible in the sidebar panel.
        """
        if request.user.is_superuser:
            groups = Group.objects.all()
            return [(group.name, group.name) for group in groups]

        elif request.user.is_teacher:
            return (
                ('is_teacher_group', 'Access Group: Teachers'),
                ('is_student_group', 'Access Group: Students'),
                ('is_mentor_group', 'Access Group: Mentors'),
            )

        else:
            return tuple()

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        if request.user.is_superuser:
            return queryset.filter(
                groups__name = self.value()
            )

        student_group_membership = Group.objects.filter(
            name="Access Group: Students",
            user=OuterRef("pk"),
        )

        teacher_group_membership = Group.objects.filter(
            name="Access Group: Teachers",
            user=OuterRef("pk"),
        )

        mentor_group_membership = Group.objects.filter(
            name="Access Group: Mentors",
            user=OuterRef("pk"),
        )
                
        queryset = queryset.annotate(
            is_student_group=Exists(student_group_membership),
            is_teacher_group=Exists(teacher_group_membership),
            is_mentor_group=Exists(mentor_group_membership)
        )
    
        return queryset.filter(
            **{self.value(): True}
        )

# CustomUserAdmin class
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom Admin for CustomUser model ensuring proper data privacy.
    """

    list_filter = ("is_staff", "is_superuser", "is_active", GroupFilter)
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
            name="Access Group: Students",
            user=OuterRef("pk"),
        )
        
        qs = qs.annotate(
            is_student_group=Exists(student_group_membership)
        ).filter(
            is_student_group=True,              # Must be a student
            groups__id__in=admin_group_ids      # Shares a group with the teacher
        ).distinct() # distinct() prevents row duplicates if users share multiple groups

        instance_ids = list(qs.values_list('id', flat=True))
        instance_ids.append(request.user.id)

        return User.objects.filter(id__in=instance_ids)