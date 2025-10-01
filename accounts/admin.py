# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "is_staff", "is_provider", "is_customer", "is_active")
    list_filter = ("is_staff", "is_provider", "is_customer", "is_active")
    search_fields = ("email", "phone")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": (
            "full_name", "phone", "district", "thana", "village", "holding_no"
        )}),
        ("Permissions", {"fields": (
            "is_active", "is_staff", "is_superuser", "is_provider", "is_customer",
            "groups", "user_permissions"
        )}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_provider", "is_customer"),
        }),
    )
