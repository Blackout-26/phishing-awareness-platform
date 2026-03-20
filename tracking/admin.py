from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import ClickEvent, SubmissionEvent

class ClickEventAdmin(SimpleHistoryAdmin):
    list_display = ('target', 'campaign', 'ip_address', 'timestamp')
    list_filter = ('campaign', 'timestamp')
    search_fields = ('target__email', 'ip_address')
    readonly_fields = ('timestamp',)

class SubmissionEventAdmin(SimpleHistoryAdmin):
    list_display = ('target', 'campaign', 'is_compromised', 'ip_address', 'timestamp')
    list_filter = ('campaign', 'is_compromised', 'timestamp')
    search_fields = ('target__email', 'ip_address')
    readonly_fields = ('timestamp',)

admin.site.register(ClickEvent, ClickEventAdmin)
admin.site.register(SubmissionEvent, SubmissionEventAdmin)