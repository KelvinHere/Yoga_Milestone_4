from django.shortcuts import render, get_object_or_404
from lessons.models import Lesson, LessonReview
from profiles.models import UserProfile

from yoga.utils import get_profile_or_none

def studio(request, id):
    """ A view for the studio """
    profile = get_profile_or_none(request)
    lesson = get_object_or_404(Lesson, lesson_id=id)
    existing_review = LessonReview.objects.filter(profile=profile, lesson=lesson).first()

    template = "studio/studio.html"
    context = {
        'profile': profile,
        'lesson': lesson,
        'existing_review': existing_review,
    }

    return render(request, template, context)
