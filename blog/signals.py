from .models import Profile
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender= User)
def profile_save(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) # name=instance.first_name + ' ' + instance.last_name, email=instance.email

