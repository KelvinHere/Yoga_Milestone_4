from django.shortcuts import render, get_object_or_404

from lessons.models import Lesson, LessonReview
from checkout.models import OrderLineItem

from yoga.utils import get_profile_or_none


def studio(request, id):
    """ A view for the studio """
    profile = get_profile_or_none(request)
    lesson = get_object_or_404(Lesson, lesson_id=id)
    existing_user_review = LessonReview.objects.filter(profile=profile, lesson=lesson).first()
    lesson_reviews = LessonReview.objects.filter(lesson=lesson)

    template = "studio/studio.html"
    context = {
        'profile': profile,
        'lesson': lesson,
        'existing_user_review': existing_user_review,
        'lesson_reviews': lesson_reviews,
    }

    return render(request, template, context)
