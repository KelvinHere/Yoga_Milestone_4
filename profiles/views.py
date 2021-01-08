from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import UserProfile
from lessons.models import Lesson, LessonItem

from .forms import ProfileForm


def profile(request):
    """ View to return the profile page """
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
        return render(request, 'profiles/profile.html', context)


def instructors(request):
    """ View to display list of instructors """
    instructor_list = UserProfile.objects.filter(is_instructor=True)

    template = 'profiles/instructors.html'
    context = {
        'instructor_list': instructor_list
    }

    return render(request, template, context)


def instructor_profile(request, instructor_id):
    """ View to disply individual instructor """
    instructor_profile = get_object_or_404(UserProfile, id=instructor_id)

    if instructor_profile.is_instructor:
        lessons = Lesson.objects.filter(instructor_profile=instructor_profile)
        


        template = 'profiles/instructor_profile.html'
        context = {
            'instructor_profile': instructor_profile,
            'lessons': lessons,
        }
        return render(request, template, context)
    else:
        return HttpResponse('This profile does not belong to an instructor', status=500)