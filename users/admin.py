from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .admin_filters import AdminLoginLogoutFilter
from .forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom configuration for the Django admin interface managing User objects.
    This customization ensures that all user-related data, including geographical
    details, can be viewed and edited directly within the Django admin.
    """

    list_display = ("username", "email", "first_name", "last_name", "phone_number", "latitude", "longitude")
    search_fields = ("username", "email", "phone_number")
    ordering = ("username",)

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    # Add the new fields to admin forms
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("phone_number", "address", "latitude", "longitude")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Extra Info", {"fields": ("phone_number", "address", "latitude", "longitude")}),
    )


# Un-register LogEntry if it has been registered
# It might be that LogEntry is already registered by Django in django.contrib.admin
try:
    admin.site.unregister(LogEntry)
except admin.sites.NotRegistered:
    pass


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for viewing and managing Django's built-in LogEntry records.
    """

    list_display = ("action_time", "user", "object_repr", "change_message", "action_flag")
    list_filter = (AdminLoginLogoutFilter, "user", "action_flag")
    search_fields = ("change_message", "user__username", "object_repr")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs
