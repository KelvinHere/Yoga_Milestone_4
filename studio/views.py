from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson, LessonReview
from checkout.models import OrderLineItem

from yoga.utils import get_profile_or_none


@login_required
def studio(request, id):
    """ A view for the studio """
    profile = get_profile_or_none(request)

    try:
        lesson = get_object_or_404(Lesson, lesson_id=id)
    except Exception as e:
        messages.error(request, 'Invalid lesson.')
        return redirect('home')

    existing_user_review = LessonReview.objects.filter(profile=profile, lesson=lesson).first()
    lesson_reviews = LessonReview.objects.filter(lesson=lesson)
    paid_lessons = OrderLineItem.objects.filter(profile=profile)

    template = "studio/studio.html"
    context = {
        'profile': profile,
        'lesson': lesson,
        'existing_user_review': existing_user_review,
        'lesson_reviews': lesson_reviews,
    }

    if paid_lessons.filter(lesson=lesson) or lesson.is_free:
        return render(request, template, context)
    else:
        messages.error(request, 'You do not own this lesson.')
        return redirect('home')