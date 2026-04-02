"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from campaigns import views as campaign_views
from email_templates import views as template_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', campaign_views.dashboard_view, name='dashboard'),
    path('campaigns/new/', campaign_views.campaign_create_view, name='campaign_create'),
    path('templates/', template_views.template_list_view, name='template_list'),
    path('templates/new/', template_views.template_create_view, name='template_create'),
    
    #Route all /track/... URLs to the tracking app
    path('track/', include('tracking.urls')),
]