from django import template
from decimal import Decimal
from django.conf import settings

register = template.Library()


@register.filter(name='deduct_sales_percentage')
def deduct_sales_percentage(value):
    site_percentage = settings.SITE_SALES_PERCENTAGE,
    print(type(site_percentage[0]))
    print(site_percentage)
    print(value)
    print(type(value))

    discount = value * Decimal(site_percentage[0]) / 100
    value -= discount
    return value