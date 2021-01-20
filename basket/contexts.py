from decimal import Decimal
from django.conf import settings

def basket_contents(request):

    basket_items = []
    total = 0
    product_count = 0

    if total >= settings.DISCOUNT_THRESHOLD:
        discount = settings.DISCOUNT_PERCENTAGE * Decimal(total / 100)
        discount_delta = settings.DISCOUNT_THRESHOLD - total
    else:
        discount = 0
        discount_delta = 0

    grand_total = total - discount

    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'discount': discount,
        'discount_delta': discount_delta,
        'grand_total': grand_total,
    }

    return context