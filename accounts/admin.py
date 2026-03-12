from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # What columns to show in the user list table
    list_display = ['username', 'email', 'role', 'is_staff']
    
    # Add the 'role' field to the user edit page
    fieldsets = UserAdmin.fieldsets + (
        ('Platform Roles', {'fields': ('role',)}),
    )
    
    # Add the 'role' field to the "Create New User" page
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Platform Roles', {'fields': ('role',)}),
    )

# Register the model and the admin class
admin.site.register(CustomUser, CustomUserAdmin)