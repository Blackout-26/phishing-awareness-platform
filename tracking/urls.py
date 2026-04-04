from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('<str:token>/', views.track_click_view, name='track_click'),
    path('landing/<str:token>/', views.simulation_landing, name='simulation_landing'),
    path('education/<str:token>/', views.education_page, name='education_page'),
]