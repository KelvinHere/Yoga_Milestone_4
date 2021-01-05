import uuid

from django.db import models
from profiles.models import InstructorProfile, StudentProfile
from django.contrib.auth.models import User


class Lesson(models.Model):
    """
    A lesson model
    """
    lesson_id = models.CharField(max_length=32, null=False, editable=False)
    instructor_name = models.ForeignKey(InstructorProfile, on_delete=models.SET_NULL,
                                        null=True, blank=True, related_name='lessons')
    lesson_name = models.CharField(max_length=32, null=False, editable=True)
    description = models.TextField(max_length=254)
    lesson_url = models.URLField(max_length=1024, null=False, blank=False)

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
    
    def get_instructor_name(self):
        return self.instructor_name


class LessonItem(models.Model):
    """
    A lesson item and its subscribed student
    """
    lesson = models.ForeignKey(Lesson, null=False, blank=False, on_delete=models.CASCADE, related_name='lessonitems')
    user = models.ForeignKey(StudentProfile, null=False, blank=False, on_delete=models.CASCADE)