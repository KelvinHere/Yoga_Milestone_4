from django.shortcuts import render


def profile(request):
    """ View to return the profile page """
    return render(request, 'profiles/profile.html')