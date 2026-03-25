from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import EmailTemplate
from .forms import EmailTemplateForm

@login_required
def template_list_view(request):
    templates = EmailTemplate.objects.all()
    return render(request, 'template_list.html', {'templates': templates})

@login_required
def template_create_view(request):
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('template_list')
    else:
        form = EmailTemplateForm()
    
    return render(request, 'template_create.html', {'form': form})