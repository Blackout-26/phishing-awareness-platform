from django import forms
from .models import EmailTemplate

class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['name', 'subject', 'body', 'sender_name', 'sender_email', 'organization']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'e.g., Urgent IT Update'}),
            'subject': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500'}),
            'body': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg h-40 outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Write your phishing email content here...'}),
            'sender_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'e.g., IT Helpdesk'}),
            'sender_email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'support@company-update.com'}),
            'organization': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg outline-none'}),
        }