from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from lessons.models import Lesson


def profile(request):
    """ View to return the profile page """
    profile = get_object_or_404(UserProfile, user=request.user)
    print('###b')
    if profile.is_instructor:
        lessons = Lesson.objects.filter(instructor_name=profile)

    context = {
        'profile': profile,
        'lessons': lessons,
    }
    return render(request, 'profiles/profile.html', context)