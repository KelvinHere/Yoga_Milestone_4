from django.shortcuts import get_object_or_404
from lessons.models import Lesson
from profiles.models import UserProfile
from checkout.models import OrderLineItem


def purchased_lessons(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    purchased = OrderLineItem.objects.filter(profile=profile)
    print('#IN HOME CONTEXT')
    context = {
        'purchased_lessons': purchased
    }
    print(purchased)
    
    return context