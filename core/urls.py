"""
URL configuration for core project.
"""
import os
from django.contrib import admin
from django.urls import path, include
from campaigns import views as campaign_views
from email_templates import views as template_views

# Fetch the custom admin URL from the environment, fallback to 'admin/' if missing
ADMIN_URL = os.environ.get('ADMIN_URL', 'admin/')

urlpatterns = [
    # Hardened Admin Route
    path(ADMIN_URL, admin.site.urls),
    
    # 🔐 NEW: Enable Django's built-in authentication URLs (login, logout, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('', campaign_views.dashboard_view, name='dashboard'),
    path('campaigns/new/', campaign_views.campaign_create_view, name='campaign_create'),
    
    # Campaign Analytics Dashboard
    path('campaigns/<int:pk>/dashboard/', campaign_views.campaign_dashboard, name='campaign_dashboard'),
    
    # Executive PDF Report
    path('campaigns/<int:pk>/report/pdf/', campaign_views.campaign_pdf_report, name='campaign_pdf_report'),
    
    path('templates/', template_views.template_list_view, name='template_list'),
    path('templates/new/', template_views.template_create_view, name='template_create'),
    
    # 🎯 NEW: Route all /targets/... URLs to the targets app
    path('targets/', include('targets.urls')),
    
    # Route all /track/... URLs to the tracking app
    path('track/', include('tracking.urls')),
]