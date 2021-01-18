import uuid

from django.db import models
from django.contrib.auth.models import User
from profiles.models import UserProfile

from django_resized import ResizedImageField


class Lesson(models.Model):
    """
    A lesson model
    """
    lesson_id = models.CharField(max_length=32, null=False, editable=False)
    instructor_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                        null=True, blank=True, related_name='lessons')
    lesson_name = models.CharField(max_length=32, null=False, editable=True)
    card_description = models.TextField(max_length=254)
    description = models.TextField(max_length=512)
    image = ResizedImageField(size=[600, 600], quality=75, crop=['middle', 'center'], force_format='JPEG', null=True, blank=True, upload_to='lesson_images/')
    rating = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)
    yoga_style = models.CharField(max_length=50, default='Yoga', null=False, blank=False)
    video_url = models.URLField(max_length=1024, null=True, blank=True)
    time = models.IntegerField(blank=True, null=True)
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def _generate_lesson_id(self):
        """
        Generate a random lesson_id using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the
        lesson_id if it hant already been set
        """
        if not self.lesson_id:
            self.lesson_id = self._generate_lesson_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.lesson_name

    def get_instructor_profile(self):
        return self.instructor_profile


class LessonImages(models.Model):
    """
    A lesson image tied to a lesson
    """
    lesson = models.ForeignKey(Lesson, null=False, blank=False, on_delete=models.CASCADE, related_name='lessonimage')
    image = models.ImageField(null=True, blank=True, upload_to='lesson_images/')

    def __str__(self):
        return f'Image for: "{self.lesson.lesson_name} by "{self.lesson.instructor_profile}"'


class LessonItem(models.Model):
    """
    A lesson item and its subscribed student
    """
    lesson = models.ForeignKey(Lesson, null=False, blank=False, on_delete=models.CASCADE, related_name='lessonitems')
    user = models.ForeignKey(UserProfile, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'Lesson "{self.lesson.lesson_name}" subscribed to by "{self.user.first_name}"'