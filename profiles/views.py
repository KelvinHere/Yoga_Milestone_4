from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import UserProfile
from lessons.models import Lesson, LessonItem


def profile(request):
    """ View to return the profile page """
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.is_instructor:
        lessons = Lesson.objects.filter(instructor_name=profile)
    else:
        # Get lesson items bound to student
        lessonItems = LessonItem.objects.filter(user=profile)
        # Put the lessons into lessons
        lessons = []
        for lesson in lessonItems:
            lessons.append(lesson.lesson)

    context = {
        'profile': profile,
        'lessons': lessons,
    }
    return render(request, 'profiles/profile.html', context)


def instructors(request):
    """ View to display list of instructors """
    instructor_list = UserProfile.objects.filter(is_instructor=True)

    for instructor in instructor_list:
        print(instructor)

    template = 'profiles/instructors.html'
    context = {
        'instructor_list': instructor_list
    }

    return render(request, template, context)


def instructor_profile(request, id):
    """ View to disply individual instructor """
    profile = get_object_or_404(UserProfile, id=id)

    if profile.is_instructor:
        template = 'profiles/instructor_profile.html'
        context = {
            'profile': profile
        }
        return render(request, template, context)
    else:
        return HttpResponse('This profile is not an instructor', status=500)