from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import EmailTemplate

class EmailTemplateAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'organization', 'subject', 'created_at')
    list_filter = ('organization', 'created_at')
    search_fields = ('name', 'subject', 'organization__name')
    
admin.site.register(EmailTemplate, EmailTemplateAdmin)