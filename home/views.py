from django.shortcuts import render

def index(request):
    """ A view to return Home page """
    template = "home/index.html"

    return render(request, template)
