from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile, Experience, Education, Contact
from django.contrib.auth.models import User
from django.conf import settings

# Signal function for creating a profile when a user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal functions for updating and deleting related models
@receiver(post_save, sender=Experience)
@receiver(post_save, sender=Education)
@receiver(post_save, sender=Contact)
def update_profile(sender, instance, created, **kwargs):
    profile = instance.profile
    profile.save()

@receiver(post_delete, sender=Experience)
@receiver(post_delete, sender=Education)
@receiver(post_delete, sender=Contact)
def delete_related(sender, instance, **kwargs):
    profile = instance.profile
    profile.save()
