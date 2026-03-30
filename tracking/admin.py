from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import ClickEvent, SubmissionEvent, TrackingLink

class TrackingLinkAdmin(SimpleHistoryAdmin):
    # This will show the token right in the main list so you don't have to click into it!
    list_display = ('target', 'campaign', 'token', 'is_clicked', 'clicked_at', 'created_at')
    list_filter = ('campaign', 'is_clicked', 'created_at')
    search_fields = ('target__email', 'token', 'campaign__name')
    readonly_fields = ('created_at',)

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

# Register all models with their custom display classes
admin.site.register(TrackingLink, TrackingLinkAdmin)
admin.site.register(ClickEvent, ClickEventAdmin)
admin.site.register(SubmissionEvent, SubmissionEventAdmin)