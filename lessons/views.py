from django.shortcuts import render


def lessons(request):
    """ View to return the lessons page """
    return render(request, 'lessons/lessons.html')