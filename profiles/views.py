from django.shortcuts import render, get_object_or_404
from lessons.models import InstructorProfile


def profile(request):
    """ View to return the profile page """

    profile = get_object_or_404(InstructorProfile, user=request.user)

    context = {
        'profile': profile
    }
    return render(request, 'profiles/profile.html', context)