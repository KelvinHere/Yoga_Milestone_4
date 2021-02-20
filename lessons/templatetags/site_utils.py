from django import template
from decimal import Decimal
from django.conf import settings

register = template.Library()


@register.filter(name='deduct_lineitem_sales_percentage')
def deduct__lineitem_sales_percentage(value, percentage):
    site_percentage = percentage,
    discount = value * Decimal(site_percentage[0]) / 100
    value -= discount
    return value
