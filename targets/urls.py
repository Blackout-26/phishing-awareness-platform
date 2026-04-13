from django.urls import path
from .views import TargetListView, TargetCreateView

urlpatterns = [
    path('', TargetListView.as_view(), name='target_list'),
    path('new/', TargetCreateView.as_view(), name='target_create'),
]