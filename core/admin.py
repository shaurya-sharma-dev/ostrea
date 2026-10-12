"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
import logging
from .models import Oyster, OysterLog, Unit, Lesson, Question

# Register your models here.
User = get_user_model()

# Get logger
logger = logging.Logger(__name__)

# Change admin site titles
admin.site.site_title = "Ostrea"
admin.site.site_header = "Ostrea"
admin.site.index_title = "Home"

# CustomUserAdmin class
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom ModelAdmin for CustomUser model.
    """

    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    readonly_fields = ("date_joined", "last_login")
    
# Custom OysterAdmin class
@admin.register(Oyster)
class OysterAdmin(admin.ModelAdmin):
    """
    Custom ModelAdmin for the Oyster model to ensure mentors can only modify their oysters.
    """

    list_display = ("name", "site_name", "site_location", "deployment_date")
    search_fields = ("name", "site_name", "site_location")
    readonly_fields = ("token",)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        
        # If this is the creation form, pre-populate the 'mentor' initial value
        if not change:
            form.base_fields["mentor"].initial = request.user

        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "mentor" and not request.user.is_superuser:
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        # Fetch default queryset.
        qs = super().get_queryset(request)
        
        # Superusers can always view oysters.
        if request.user.is_superuser:
            return qs
        
        is_mentor = request.user.is_mentor

        if not is_mentor:
            # If it is not a mentor, return an empty queryset.
            # The user must have been given permissions incorrectly.
            logger.warning("A user has view oysters permission without being a superuser or mentor. The system has not given them access to oysters.")
            return Oyster.objects.none()

        qs = qs.filter(
            mentor__id=request.user.id
        ).distinct()

        return qs

    def delete_queryset(self, request, queryset):
        # Intersect the submitted items with what the user is allowed to see
        allowed_queryset = queryset & self.get_queryset(request)
        
        # Pass the filtered queryset to the default delete logic
        super().delete_queryset(request, allowed_queryset)

# Custom OysterLogAdmin class
@admin.register(OysterLog)
class OysterLogAdmin(admin.ModelAdmin):
    list_display = ("oyster", "date", "salinity", "temperature", "shell_diameter", "weight")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "oyster" and not request.user.is_superuser:
            kwargs["queryset"] = Oyster.objects.filter(mentor=request.user)
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        # Fetch default queryset.
        qs = super().get_queryset(request)
        
        # Superusers can view all logs.
        if request.user.is_superuser:
            return qs
        
        is_mentor = request.user.is_mentor

        if not is_mentor:
            # If the user is not a mentor, return an empty queryset.
            # The user must have been given permissions incorrectly.
            logger.warning("A user has view OysterLog permission without being a superuser or mentor. The system has not given them access to OysterLogs.")
            return OysterLog.objects.none()
        
        qs = qs.filter(
            oyster__mentor=request.user, # The mentor of the oyster must be the mentor currently logged in.
        )

        return qs

    def delete_queryset(self, request, queryset):
        # Intersect the submitted items with what the user is allowed to see
        allowed_queryset = queryset & self.get_queryset(request)
        
        # Pass the filtered queryset to the default delete logic
        super().delete_queryset(request, allowed_queryset)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("name", "unit")
    list_filter = ("unit",)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("lesson", "text", "correct_choice")
    list_filter = ("lesson",)

admin.site.register([Unit])