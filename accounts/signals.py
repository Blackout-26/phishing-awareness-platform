from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def assign_user_group(sender, instance, created, **kwargs):
    """
    Automatically assigns the user to a Django Group based on their role.
    Creates the group if it doesn't exist yet.
    """
    # Clear existing groups to prevent overlapping access if a role is changed
    instance.groups.clear()
    
    if instance.role == 'admin':
        group, _ = Group.objects.get_or_create(name='Administrator')
        instance.groups.add(group)
    elif instance.role == 'analyst':
        group, _ = Group.objects.get_or_create(name='Security Analyst')
        instance.groups.add(group)