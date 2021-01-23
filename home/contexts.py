from yoga.utils import get_profile_or_none
from lessons.models import Lesson
from profiles.models import UserProfile
from checkout.models import OrderLineItem


def purchased_lessons(request):

    profile = get_profile_or_none(request)
    purchased = None

    if profile:
        purchased = OrderLineItem.objects.filter(profile=profile)

    context = {
        'purchased_lessons': purchased
    }
    print(purchased)

    return context
