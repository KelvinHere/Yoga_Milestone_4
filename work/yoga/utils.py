"""
Utility functions to be used by entire site
"""
from django.conf import settings
from django.shortcuts import get_object_or_404

from profiles.models import UserProfile
from lessons.models import Lesson


def get_profile_or_none(request):
    """ Function returns a valid UserProfile or None """
    try:
        return UserProfile.objects.get(user=request.user)
    except Exception:
        return None


def discount_delta_zero(request):
    """ Returns True if discount has been reached """
    total = 0
    basket = request.session.get('basket', {})
    discount_delta_zero = False

    for lesson_id in basket:
        if Lesson.objects.filter(lesson_id=lesson_id).exists():
            lesson = get_object_or_404(Lesson, lesson_id=lesson_id)
            total += lesson.price

    if total >= settings.DISCOUNT_THRESHOLD:
        discount_delta_zero = True

    return discount_delta_zero
