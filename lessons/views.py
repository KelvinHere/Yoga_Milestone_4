from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from lessons.models import Lesson, LessonItem


def lessons(request):
    """ View to return the lessons page """
    profile = get_object_or_404(UserProfile, user=request.user)

    template = 'lessons/lessons.html'

    context = {
        'profile': profile,
    }

    return render(request, template, context)


def my_lessons(request):
    """ View to return the lessons page """
    print('IN VIEW####################')
    profile = get_object_or_404(UserProfile, user=request.user)

    template = 'lessons/my_lessons.html'

    # Get the lesson field only of the Lesson items linked to the current profile

    # Get lesson items bound to student
    lessonItems = LessonItem.objects.filter(user=profile)
    lessons = []
    for lesson in lessonItems:
        lessons.append(lesson.lesson)

    context = {
        'profile': profile,
        'lessons': lessons,
    }

    return render(request, template, context)
