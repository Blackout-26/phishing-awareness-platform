from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import TargetUser

class TargetUserAdmin(SimpleHistoryAdmin):
    list_display = ('email', 'first_name', 'department', 'organization', 'status')
    list_filter = ('organization', 'department', 'status')
    search_fields = ('email', 'first_name', 'last_name', 'organization__name')
    list_editable = ('status',)
    
admin.site.register(TargetUser, TargetUserAdmin)