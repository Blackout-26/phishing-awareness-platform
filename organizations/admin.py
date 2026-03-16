from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Organization

class OrganizationAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'owner', 'contact_email', 'created_at')
    search_fields = ('name', 'contact_email')
    list_filter = ('created_at',)

# Register the model and the admin class
admin.site.register(Organization, OrganizationAdmin)