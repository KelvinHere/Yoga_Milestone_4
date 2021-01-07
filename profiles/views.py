from django.shortcuts import render, get_object_or_404
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