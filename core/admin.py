from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.
User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom Admin for CustomUser model ensuring proper data privacy.
    """
    
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
            return User.objects.none()

        admin_group_ids = request.user.groups.values_list('id', flat=True)
        
        return qs.filter(
            is_student=True,                    # Must be a student
            groups__id__in=admin_group_ids      # Shares a group with the teacher
        ).distinct() # distinct() prevents row duplicates if users share multiple groups