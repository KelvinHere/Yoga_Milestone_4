from django.shortcuts import render, get_object_or_404, redirect
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
    except Exception:
        messages.error(request, 'Invalid lesson.')
        return redirect('home')

    existing_user_review = LessonReview.objects.filter(
        profile=profile, lesson=lesson).first()
    paid_lessons = OrderLineItem.objects.filter(profile=profile)
    # Get and sort reviews
    lesson_reviews = LessonReview.objects.filter(
        lesson=lesson).exclude(profile=profile)
    lesson_reviews = lesson_reviews.order_by('-date')
    my_review = LessonReview.objects.filter(lesson=lesson, profile=profile)

    template = "studio/studio.html"
    context = {
        'profile': profile,
        'lesson': lesson,
        'existing_user_review': existing_user_review,
        'lesson_reviews': lesson_reviews,
        'my_review': my_review,
    }

    if (paid_lessons.filter(lesson=lesson) or lesson.is_free or
            lesson.instructor_profile == profile or
            profile.user.is_superuser):
        return render(request, template, context)
    else:
        messages.error(request, 'You do not own this lesson.')
        return redirect('home')
