from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, reverse
from lessons.models import LessonItem
from profiles.models import UserProfile, User

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


def superuser_admin(request):
    """ View for superuser admin, shows user requests """
    profile = get_profile_or_none(request)

    if profile:
        if profile.user.is_superuser:
            template = "home/superuser_admin.html"
            user_requests = UserProfile.objects.filter(is_instructor=False, requested_instructor_status=True)
            instructors = UserProfile.objects.filter(is_instructor=True)

            context = {
                'profile': profile,
                'user_requests': user_requests,
                'instructors': instructors
            }
            return render(request, template, context)
    else:
        return HttpResponse('You are not authorised to view this page', status=401)


def update_instructor_status(request, user_to_update, status):
    """ Sets or unsets instructor status """
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.user.is_superuser:
        update_user = User.objects.get(username=user_to_update)
        update_profile = UserProfile.objects.get(user=update_user)
        if status == 'accept':
            update_profile.is_instructor = True
            update_profile.requested_instructor_status = True
            update_profile.save()
        else:
            update_profile.is_instructor = False
            update_profile.requested_instructor_status = False
            update_profile.save()
        return redirect(reverse('superuser_admin'))
    else:
        return HttpResponse('You are not authorised to perform this action', status=401)