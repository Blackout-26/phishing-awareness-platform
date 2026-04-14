from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import TargetUser

class TargetListView(ListView):
    model = TargetUser
    template_name = 'targets/target_list.html'
    context_object_name = 'targets'

class TargetCreateView(CreateView):
    model = TargetUser
    template_name = 'targets/target_create.html'
    # Updated to match the exact fields in your TargetUser model
    fields = ['email', 'first_name', 'last_name', 'department', 'status', 'organization']
    success_url = reverse_lazy('target_list')