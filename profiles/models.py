from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Model for the user profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    is_instructor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
