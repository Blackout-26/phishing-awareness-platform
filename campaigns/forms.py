from django import forms
from .models import Campaign

class CampaignCreateForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description', 'start_date', 'end_date', 'organization', 'template']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg h-24 outline-none', 'rows': 3}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-4 py-2 border rounded-lg outline-none'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-4 py-2 border rounded-lg outline-none'}),
            'organization': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg outline-none'}),
            'template': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg outline-none'}),
        }