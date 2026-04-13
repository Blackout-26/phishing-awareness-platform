from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Target # Adjust if your model name is different

class TargetListView(ListView):
    model = Target
    template_name = 'targets/target_list.html'
    context_object_name = 'targets'

class TargetCreateView(CreateView):
    model = Target
    template_name = 'targets/target_create.html'
    fields = ['first_name', 'last_name', 'email', 'organization'] # Adjust to match your model fields
    success_url = reverse_lazy('target_list')