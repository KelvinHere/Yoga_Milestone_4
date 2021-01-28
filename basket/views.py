from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from lessons.models import Lesson

import json


@login_required
def view_basket(request):
    """ A view to view the basket """
    template = 'basket/basket.html'
    return render(request, template)


@login_required
def add_to_basket(request):
    """ Add a lesson to the basket """
    basket = request.session.get('basket', {})

    if request.method == 'POST':
        if 'lesson_id' in request.POST:
            lesson_id = request.POST.get('lesson_id')
            # If lesson id is invalid
            if not Lesson.objects.get(lesson_id=lesson_id):
                messages.error(request, f"Invalid lesson, please select lessons from the lessons page")
                return redirect(reverse('home'))
            # If lesson is not in basket
            if lesson_id not in list(basket.keys()):
                basket[lesson_id] = 1
                request.session['basket'] = basket
                json_response = json.dumps({'item_added': 'True'})
                return HttpResponse(json_response, content_type='application/json')
            # If lesson is in basket
            else:
                json_response = json.dumps({'item_added': 'already_added'})
                return HttpResponse(json_response, content_type='application/json')
        # If incorrect POST data
        else:
            messages.error(request, f"Invalid request, please select lessons from the lessons page")
            return redirect(reverse('home'))
    # If not post request
    else:
        messages.error(request, f"Invalid request, please select lessons from the lessons page")
        return redirect(reverse('home'))


@login_required
def remove_from_basket(request):
    """ Removes item from basket """
    basket = request.session.get('basket', {})

    try:
        if 'lesson_id' in request.POST:
            lesson_id = request.POST.get('lesson_id')
            basket.pop(lesson_id)
            request.session['basket'] = basket
            json_response = json.dumps({'item_removed': 'True'})
            return HttpResponse(json_response, content_type='application/json')
        else:
            messages.error(request, "Invalid request, no lesson was specified for deletion")
            return redirect(reverse('basket'))
    except Exception as e:
        messages.error(request, f"Something went wrong, please contact {settings.DEFAULT_FROM_EMAIL} if you need assistance.")
        return redirect(reverse('basket'))
