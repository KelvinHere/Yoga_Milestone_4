from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from lessons.models import Subscription, LessonReviewFlagged
from profiles.models import UserProfile

from yoga.utils import get_profile_or_none


def index(request):
    """ A view to return Home page """
    profile = get_profile_or_none(request)
    subscribed_lessons = False

    if profile:
        if Subscription.objects.filter(user=profile).count() > 0:
            subscribed_lessons = True

    template = "home/index.html"
    context = {
        'profile': profile,
        'subscribed_lessons': subscribed_lessons,
    }

    return render(request, template, context)


@login_required
def superuser_admin(request):
    """ View for superuser admin, shows user requests """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only administrators can do this')
        return redirect(reverse('home'))

    profile = get_object_or_404(UserProfile, user=request.user)
    template = "home/superuser_admin.html"
    user_requests = UserProfile.objects.filter(
        is_instructor=False,
        requested_instructor_status=True
        )
    instructors = UserProfile.objects.filter(is_instructor=True)
    flagged_reviews = LessonReviewFlagged.objects.all().order_by('review')

    # Split results into dict of reviews that
    # contain the users who flagged them
    sorted_flagged_reviews = {}
    total_flags = 0
    for flagged in flagged_reviews:
        if flagged.review.pk not in sorted_flagged_reviews:
            sorted_flagged_reviews[flagged.review.pk] = {
                'review_pk': flagged.review.pk,
                'lesson_name': flagged.review.lesson.lesson_name,
                'reviewer': flagged.review.profile.user.username,
                'review': flagged.review.review,
                'flaggers': [],
                }
        sorted_flagged_reviews[flagged.review.pk]['flaggers'].append(
            flagged.profile.user.username)
        total_flags += 1

    context = {
        'profile': profile,
        'user_requests': user_requests,
        'instructors': instructors,
        'flagged_reviews': flagged_reviews,
        'sorted_flagged_reviews': sorted_flagged_reviews,
        'total_flags': total_flags,
        }

    return render(request, template, context)


@login_required
def update_instructor_status(request, user_to_update, status):
    """ Sets or unsets instructor status """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only administrators can do this')
        return redirect(reverse('home'))

    try:
        update_profile = UserProfile.objects.get(user__username=user_to_update)
    except Exception:
        messages.error(request, 'User does not exist.')
        return redirect(reverse('superuser_admin'))

    if status == 'accept':
        update_profile.is_instructor = True
        update_profile.requested_instructor_status = True
        update_profile.save()
    else:
        update_profile.is_instructor = False
        update_profile.requested_instructor_status = False
        update_profile.save()
        messages.error(request, 'Submitted invalid status.')
    return redirect(reverse('superuser_admin'))


def handle_404(request, exception):
    """ 404 page not found view """
    return render(request, '/404.html', status=404)
