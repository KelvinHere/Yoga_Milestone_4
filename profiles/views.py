from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, reverse
from .models import UserProfile
from lessons.models import Lesson, LessonItem
from django.contrib import messages

from yoga.utils import get_profile_or_none

from .forms import ProfileForm


def profile(request, show_profile_error_toast=False):
    """ View to view the personal profile page of the logged in user """
    profile = get_object_or_404(UserProfile, user=request.user)
    profile_complete = profile.test_profile_is_complete()

    if 'error' in request.GET:
        messages.warning(request, 'You must complete your profile first!')

    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'profile_complete': profile_complete,
    }
    return render(request, template, context)


def edit_profile(request):
    """ View to edit the personal profile page of the logged in user """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
        return redirect('profile')

    else:
        form = ProfileForm(instance=profile)

        context = {
            'profile': profile,
            'form': form,
        }
        return render(request, 'profiles/edit_profile.html', context)


def instructor_profile(request, instructor_id):
    """ View to disply an instructor and their lessons to a user """
    instructor_profile = get_object_or_404(UserProfile, id=instructor_id)
    profile = get_profile_or_none(request)

    # Does profile belong to a instructor
    if instructor_profile.is_instructor:
        lessons = Lesson.objects.filter(instructor_profile=instructor_profile)
    else:
        return HttpResponse('This profile does not belong to an instructor', status=500)

    # Get a list of subscribed lesson IDs for current user
    subscribed_lesson_list = []
    if request.user.is_authenticated:
        subscribed_lessons = LessonItem.objects.filter(user=profile)
        for each in subscribed_lessons:
            subscribed_lesson_list.append(each.lesson.lesson_id)

    # If authenticated get a list of paid lessons
    paid_lesson_list = []
    if request.user.is_authenticated:
        lesson_items = LessonItem.objects.filter(user=profile, paid_for=True)
        for lesson_item in lesson_items:
            paid_lesson_list.append(lesson_item.lesson.lesson_id)

    template = 'profiles/instructor_profile.html'
    context = {
        'profile': profile,
        'instructor_profile': instructor_profile,
        'lessons': lessons,
        'subscribed_lesson_list': subscribed_lesson_list,
        'paid_lesson_list': paid_lesson_list,
    }
    return render(request, template, context)


def instructors(request):
    """ View to display list of instructors """
    instructor_list = UserProfile.objects.filter(is_instructor=True)

    template = 'profiles/instructors.html'
    context = {
        'instructor_list': instructor_list
    }

    return render(request, template, context)

def request_instructor_status(request, status):
    """ View for user to request to become an instructor """
    profile = get_object_or_404(UserProfile, user=request.user)

    if status == 'request':
        profile.requested_instructor_status = True
        profile.save()
    else:
        profile.requested_instructor_status = False
        profile.save()

    return redirect(reverse('profile'))
