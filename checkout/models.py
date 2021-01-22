import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings

from profiles.models import UserProfile
from lessons.models import Lesson


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    profile = models.ForeignKey(UserProfile, null=False, blank=False, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    stripe_id = models.CharField(max_length=254, null=False, blank=False, default='')
    original_basket = models.TextField(null=False, blank=False, default='')

    def _generate_order_number(self):
        """
        Generate a random order_number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total including discount
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.DISCOUNT_THRESHOLD:
            discount_amount = 0
        else:
            discount_amount = settings.DISCOUNT_PERCENTAGE * (self.order_total / 100)
        self.grand_total = (self.order_total - discount_amount)
        self.save()

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the
        order_number if it hasn't already been set
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    lesson = models.ForeignKey(Lesson, null=False, blank=False, on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, null=False, blank=False, on_delete=models.CASCADE)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the
        line_item total and update total order
        """
        self.lineitem_total = self.lesson.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order no: {self.order.order_number} - Item: {self.lesson.lesson_name}'