from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from lessons.models import LessonItem
from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    print('#### Reciever fired')
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.order.update_total()


@receiver(pre_delete, sender=OrderLineItem)
def delete_associated_subscriptions(sender, instance, using, **kwargs):
    """
    Delete all subscriptions to paid lesson being deleted
    """
    print('#Pre delete')
    print(instance)
    LessonItem.objects.filter(user=instance.profile, lesson=instance.lesson).delete()