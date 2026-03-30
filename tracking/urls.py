from django.urls import path
from . import views

urlpatterns = [
    path('t/<str:token>/', views.track_click_view, name='track_click'),
    
    path('landing/<str:token>/', views.simulation_landing_placeholder, name='simulation_landing'),
]