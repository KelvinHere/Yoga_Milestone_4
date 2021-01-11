from django.shortcuts import render
from lessons.models import LessonItem

from yoga.utils import get_profile_or_none

def index(request):
    """ A view to return Home page """
    profile = get_profile_or_none(request)
    subscribed_lessons = False

    if profile:
        if LessonItem.objects.filter(user=profile).count() > 0:
            subscribed_lessons = True

    template = "home/index.html"
    context = {
        'profile': profile,
        'subscribed_lessons': subscribed_lessons,
    }

    return render(request, template, context)
