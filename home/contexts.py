from yoga.utils import get_profile_or_none
from lessons.models import Lesson
from profiles.models import UserProfile
from checkout.models import OrderLineItem


def purchased_lessons(request):

    profile = get_profile_or_none(request)
    purchased = None
    purchased_lesson_ids = []

    if profile:
        purchased = OrderLineItem.objects.filter(profile=profile)
        if purchased:
            for item in purchased:
                purchased_lesson_ids.append(item.lesson.lesson_id)

    context = {
        'purchased_lessons': purchased,
        'purchased_lesson_ids': purchased_lesson_ids,
    }
    print(purchased)

    return context
