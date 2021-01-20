from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404

from lessons.models import Lesson

def basket_contents(request):

    basket_items = []
    total = 0
    product_count = 0
    basket = request.session.get('basket', {})

    for lesson_id in basket:
        lesson = get_object_or_404(Lesson, lesson_id=lesson_id)
        total += lesson.price
        product_count += 1
        basket_items.append({
            'lesson': lesson,
            'price': lesson.price,
        })


    if total >= settings.DISCOUNT_THRESHOLD:
        discount = settings.DISCOUNT_PERCENTAGE * Decimal(total / 100)
    else:
        discount = 0
        discount_delta = settings.DISCOUNT_THRESHOLD - total

    grand_total = total - discount

    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'discount': discount,
        'discount_delta': discount_delta,
        'discount_percentage': settings.DISCOUNT_PERCENTAGE,
        'grand_total': grand_total,
    }

    return context