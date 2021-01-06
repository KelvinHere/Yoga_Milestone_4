from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from lessons.models import Lesson, LessonItem


def lessons(request):
    """ View to return the lessons page """
    profile = get_object_or_404(UserProfile, user=request.user)
    all_lessons = Lesson.objects.all()
    subscribed_lessons = LessonItem.objects.filter(user=profile)
    template = 'lessons/lessons.html'
    context = {
        'profile': profile,
        'all_lessons': all_lessons,
        'subscribed_lessons': subscribed_lessons,
    }

    return render(request, template, context)


def my_lessons(request):
    """ View to return the lessons page """
    profile = get_object_or_404(UserProfile, user=request.user)
    template = 'lessons/my_lessons.html'

    lessonItems = LessonItem.objects.filter(user=profile)

    context = {
        'profile': profile,
        'lessons': lessons,
        'lesson_items': lessonItems,
    }

    return render(request, template, context)


def instructor_created_lessons(request):
    """ View to return the lessons page """

    profile = get_object_or_404(UserProfile, user=request.user)
    template = 'lessons/instructor_created_lessons.html'

    # Get lesson items bound to student
    instructor_created_lessons = Lesson.objects.filter(instructor_name=profile)


    context = {
        'profile': profile,
        'instructor_created_lessons': instructor_created_lessons,
    }

    return render(request, template, context)


def subscribe_lesson(request, id):
    """ View to subscribe to a lesson """
    profile = get_object_or_404(UserProfile, user=request.user)
    lesson = get_object_or_404(Lesson, pk=id)
    if not LessonItem.objects.filter(lesson=lesson, user=profile).exists():
        LessonItem.objects.create(lesson=lesson, user=profile)

    return redirect('lessons')


def unsubscribe_lesson(request, id):
    """ View to remove a subscribed lesson from a UserProfile """
    unsubscribe = get_object_or_404(LessonItem, pk=id)

    unsubscribe.delete()
    return redirect('my_lessons')
