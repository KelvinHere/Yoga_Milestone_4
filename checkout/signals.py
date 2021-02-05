from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from lessons.models import Subscription
from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.order.update_total()
    lesson_subscription = Subscription(lesson=instance.lesson,
                                       user=instance.profile)
    lesson_subscription.save()


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
    Subscription.objects.filter(user=instance.profile,
                                lesson=instance.lesson).delete()
