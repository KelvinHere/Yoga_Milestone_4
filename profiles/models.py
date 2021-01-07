from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Model for the user profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    is_instructor = models.BooleanField(default=False)
    profile_description = models.TextField()
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    rating = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile through signals/reciever
    Needs post_save and reviever importing
    """
    print('##### in signals')
    if created:
        UserProfile.objects.create(user=instance)
    # If user exists just save the profile
    instance.userprofile.save()
