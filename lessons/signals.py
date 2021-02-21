from django.db.models.signals import post_delete
from django.dispatch import receiver

from lessons.models import LessonReview


@receiver(post_delete, sender=LessonReview)
def update_on_delete(sender, instance, **kwargs):
    """
    Update lesson rating on review deleted
    """
    print('#REVIEW DELETED IN POST DELETE')
    instance.lesson._update_rating()
