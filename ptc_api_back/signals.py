"""
The signals enable the server to do some actions whenever an event occurs.
Here, we catch the saving of an User instance, or a Trip instance.
"""
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from ptc_api_back.models import Profile, Trip

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    When a User object is created, a linked Profile object is created automatically.
    """
    if created:
        Profile.objects.create(traveler=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    When a User object is saved, its profile is saved too.
    """
    instance.profile.save()

@receiver(post_save, sender=Trip)
def create_trip_tasks(sender, instance, created, **kwargs):
    """
    When a Trip object is created, the tasks asociated are created automatically.
    """
    if created:
        instance.generate_tasks()
