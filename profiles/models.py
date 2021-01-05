from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    """
    An extended profile for students
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.user.username


class InstructorProfile(models.Model):
    """
    An extended profile for students
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.user.username