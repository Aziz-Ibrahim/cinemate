from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(f"DEBUG: Profile created via signal for {instance.username}")

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Save the Profile when the User is saved."""
    instance.profile.save()
