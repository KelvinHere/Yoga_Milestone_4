from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_resized import ResizedImageField


class UserProfile(models.Model):
    """
    Model for the user profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    is_instructor = models.BooleanField(default=False)
    requested_instructor_status = models.BooleanField(default=False)
    card_description = models.TextField(max_length=256, blank=True, default='')
    profile_description = models.TextField(max_length=650, blank=True, default='')
    image = ResizedImageField(
        size=[600, 600], quality=75, crop=['middle', 'center'],
        force_format='JPEG', null=True, blank=True,
        upload_to='profile_images/'
        )
    rating = models.DecimalField(
        max_digits=5, decimal_places=0, null=True, blank=True
        )
    lesson_count = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.user.username

    def test_profile_is_complete(self):
        """ Tests to see if the profile is complete returns bool """
        if (self.first_name and self.last_name and
                self.profile_description and self.image):
            return True
        else:
            return False

    def _update_rating(self, lessons_by_this_instructor):
        """ Update profile rating from lessons average score """
        if lessons_by_this_instructor:
            total_rating = 0
            no_of_lessons_with_reviews = 0
            for lesson in lessons_by_this_instructor:
                if lesson.rating is not None:
                    total_rating += lesson.rating
                    no_of_lessons_with_reviews += 1
            if no_of_lessons_with_reviews > 0:
                new_rating = total_rating / no_of_lessons_with_reviews
                self.rating = new_rating
            else:
                self.rating = None
        else:
            self.rating = None
        self.save()

    def _update_lesson_count(self, total_lessons):
        """ Update lesson count """
        self.lesson_count = total_lessons
        self.save()


#@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile through signals/reciever
    Needs post_save and reviever importing
    """
    if created:
        UserProfile.objects.create(user=instance)
    # If user exists just save the profile
    instance.userprofile.save()
