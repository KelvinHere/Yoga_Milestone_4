import uuid

from django.db import models
from profiles.models import UserProfile

from django_resized import ResizedImageField
from datetime import datetime


class Lesson(models.Model):
    """
    A lesson model
    """
    lesson_id = models.CharField(max_length=32,
                                 null=False,
                                 editable=False)
    instructor_profile = models.ForeignKey(UserProfile,
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True,
                                           related_name='lessons')
    lesson_name = models.CharField(max_length=32,
                                   null=False,
                                   editable=True)
    card_description = models.TextField(max_length=254)
    description = models.TextField(max_length=2048)
    image = ResizedImageField(size=[600, 600],
                              quality=75,
                              crop=['middle', 'center'],
                              force_format='JPEG',
                              upload_to='lesson_images/')
    rating = models.DecimalField(max_digits=5,
                                 decimal_places=0,
                                 null=True, blank=True)
    video_url = models.URLField(max_length=1024,
                                blank=False,
                                null=False)
    time = models.IntegerField(blank=False, null=False)
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=6,
                                decimal_places=2,
                                blank=False,
                                null=False,
                                default=0.00)

    def _generate_lesson_id(self):
        """
        Generate a random lesson_id using UUID
        """
        return uuid.uuid4().hex.upper()

    def _update_rating(self):
        """
        Finds all reviews and updates average review
        """
        reviews = LessonReview.objects.filter(lesson=self)
        if reviews:
            total_rating = 0
            no_of_reviews = 0
            for review in reviews:
                total_rating += int(review.rating)
                no_of_reviews += 1
            new_rating = total_rating / no_of_reviews
            self.rating = new_rating
        else:
            self.rating = None
        self.save()
        # Send a list of all lessons by this instructor to
        # its profile for rating update
        lessons_by_this_instructor = Lesson.objects.filter(
            instructor_profile=self.instructor_profile)

        self.instructor_profile._update_rating(lessons_by_this_instructor)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the
        lesson_id if it hasn't already been set
        """
        if not self.lesson_id:
            self.lesson_id = self._generate_lesson_id()
        # If a price has been entered over Zero, is free field removed
        if self.price > 0:
            self.is_free = False
        else:
            self.is_free = True
        super().save(*args, **kwargs)
        total_lessons = Lesson.objects.filter(
            instructor_profile=self.instructor_profile).count()

        self.instructor_profile._update_lesson_count(total_lessons)

    def __str__(self):
        return self.lesson_name

    def get_instructor_profile(self):
        return self.instructor_profile


class Subscription(models.Model):
    """
    A lesson item and its subscribed student
    """
    lesson = models.ForeignKey(Lesson,
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE,
                               related_name='Subscriptions')
    user = models.ForeignKey(UserProfile,
                             null=False,
                             blank=False,
                             on_delete=models.CASCADE)

    def __str__(self):
        return (f'Lesson "{self.lesson.lesson_name}" subscribed to '
                f'by "{self.user}"')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class LessonReview(models.Model):
    """
    A lesson review
    """
    profile = models.ForeignKey(UserProfile,
                                null=False,
                                on_delete=models.CASCADE,
                                blank=False,
                                related_name='reviewer')
    lesson = models.ForeignKey(Lesson,
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE,
                               related_name='reviewedLesson')
    review = models.TextField(max_length=512)
    rating = models.IntegerField()
    date = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        """
        Force linked lesson model to recalculate average
        score after it has been saved
        """
        super().save(*args, **kwargs)
        self.lesson._update_rating()

    def __str__(self):
        return f'Review of "{self.lesson.lesson_name}" by "{self.profile}"'


class LessonReviewFlagged(models.Model):
    """
    A flag for a lesson review that may
    contain inapropriate content
    """
    profile = models.ForeignKey(UserProfile,
                                null=False,
                                on_delete=models.CASCADE,
                                blank=False,
                                related_name='profileThatFlaggedReview')
    review = models.ForeignKey(LessonReview,
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE,
                               related_name='flaggedReview')

    def __str__(self):
        return (f'Review of "{self.review.lesson.lesson_name}" '
                f'flagged by "{self.profile}"')

    class Meta:
        verbose_name_plural = "Lesson Reviews Flagged"
