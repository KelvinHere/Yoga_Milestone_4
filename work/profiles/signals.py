from django.db.models.signals import post_delete
from django.dispatch import receiver

from lessons.models import Lesson


@receiver(post_delete, sender=Lesson)
def update_on_delete(sender, instance, **kwargs):
    """
    Update instructor rating on lesson deleted
    """
    instructor = instance.instructor_profile

    lessons_by_this_instructor = Lesson.objects.filter(
        instructor_profile=instructor)
    total_lessons = lessons_by_this_instructor.count()

    instance.instructor_profile._update_lesson_count(total_lessons)
    instance.instructor_profile._update_rating(lessons_by_this_instructor)
