from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404

from lessons.models import Lesson

def basket_contents(request):

    basket_items = []
    basket_item_ids = []
    total = 0
    product_count = 0
    basket = request.session.get('basket', {})
    invalid_lessons_to_remove = []

    for lesson_id in basket:
        # Check lesson_id is valid, remove from basket if not
        if not Lesson.objects.filter(lesson_id=lesson_id).exists():
            invalid_lessons_to_remove.append(lesson_id)
        # Add lesson to basket items
        else:
            lesson = get_object_or_404(Lesson, lesson_id=lesson_id)
            total += lesson.price
            product_count += 1
            basket_items.append({
                'lesson': lesson,
                'price': lesson.price,
            })
            basket_item_ids.append(lesson.lesson_id)

    # Remove any invalid lessons
    if invalid_lessons_to_remove:
        for invalid_lesson in invalid_lessons_to_remove:
            basket.pop(invalid_lesson)
        invalid_lessons_to_remove = []

    if total >= settings.DISCOUNT_THRESHOLD:
        discount = settings.DISCOUNT_PERCENTAGE * Decimal(total / 100)
    else:
        discount = 0
        discount_delta = settings.DISCOUNT_THRESHOLD - total

    grand_total = total - discount

    context = {
        'basket_items': basket_items,
        'basket_item_ids': basket_item_ids,
        'total': total,
        'product_count': product_count,
        'discount': discount,
        'discount_delta': discount_delta,
        'discount_percentage': settings.DISCOUNT_PERCENTAGE,
        'grand_total': grand_total,
    }

    return context