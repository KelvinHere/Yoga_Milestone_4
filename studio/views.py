from django.shortcuts import render, get_object_or_404
from lessons.models import Lesson
from profiles.models import UserProfile

def studio(request, id):
    """ A view for the studio """
    profile = get_object_or_404(UserProfile, user=request.user)
    lesson = get_object_or_404(Lesson, lesson_id=id)

    template = "studio/studio.html"
    context = {
        'profile': profile,
        'lesson': lesson,
    }

    return render(request, template, context)