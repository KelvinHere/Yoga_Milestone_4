from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from lessons.models import Lesson, LessonItem

from .forms import CreateLessonForm


def lessons(request):
    """ View to return the lessons page """
    profile = get_object_or_404(UserProfile, user=request.user)
    all_lessons = Lesson.objects.all()
    
    # Get a list of subscribed lesson IDs for current user
    subscribed_lessons = LessonItem.objects.filter(user=profile)
    subscribed_lesson_list = []
    for each in subscribed_lessons:
        subscribed_lesson_list.append(each.lesson.lesson_id)

    template = 'lessons/lessons.html'
    context = {
        'profile': profile,
        'all_lessons': all_lessons,
        'subscribed_lesson_list': subscribed_lesson_list,
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
    # Get needed fields
    profile = get_object_or_404(UserProfile, user=request.user)
    lesson = get_object_or_404(Lesson, pk=id)

    # Create LessonItem if it does not already exist
    if not LessonItem.objects.filter(lesson=lesson, user=profile).exists():
        LessonItem.objects.create(lesson=lesson, user=profile)

    return redirect('lessons')


def unsubscribe_lesson(request, id):
    """ View to remove a subscribed lesson from a UserProfile """
    unsubscribe = get_object_or_404(LessonItem, pk=id)

    unsubscribe.delete()
    return redirect('my_lessons')


def create_lesson(request):
    """ View to create a lesson """
    print('#IN CREATE LESSON')
    profile = get_object_or_404(UserProfile, user=request.user)
    form = CreateLessonForm(initial={'instructor_name':profile})
    

    template = 'lessons/create_lesson.html'

    context = {
        'form': form
    }

    return render(request, template, context)