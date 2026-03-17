from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Campaign

class CampaignAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'organization', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'organization', 'created_at')
    search_fields = ('name', 'organization__name')
    
    # Make the list view easily editable for statuses
    list_editable = ('status',)

admin.site.register(Campaign, CampaignAdmin)