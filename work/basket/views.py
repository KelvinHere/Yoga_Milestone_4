from django.shortcuts import (render,
                              HttpResponse,
                              redirect,
                              reverse,
                              get_object_or_404)
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from profiles.models import UserProfile
from lessons.models import Lesson
from checkout.models import OrderLineItem
from yoga.utils import discount_delta_zero

import json


@login_required
def view_basket(request):
    """ A view to view the basket """
    template = 'basket/basket.html'

    context = {
        'show_discount_banner': True,
    }

    return render(request, template, context)


@login_required
def add_to_basket(request):
    """ Add a lesson to the basket """
    profile = get_object_or_404(UserProfile, user=request.user)
    basket = request.session.get('basket', {})

    if request.method == 'POST':
        if 'lesson_id' in request.POST:
            lesson_id = request.POST.get('lesson_id')
            # If lesson id is invalid
            if not Lesson.objects.filter(lesson_id=lesson_id).exists():
                json_response = json.dumps({'item_added': 'invalid_item'})
                return HttpResponse(json_response,
                                    content_type='application/json')

            lesson = Lesson.objects.get(lesson_id=lesson_id)
            # If lesson is free
            if lesson.is_free:
                json_response = json.dumps(
                    {'item_added': 'invalid_item_is_free'})

                return HttpResponse(json_response,
                                    content_type='application/json')

            # If already owned
            if OrderLineItem.objects.filter(lesson=lesson,
                                            profile=profile).exists():
                json_response = json.dumps({'item_added': 'already_owned'})
                return HttpResponse(json_response,
                                    content_type='application/json')

            # If lesson is not in basket
            if lesson_id not in list(basket.keys()):
                basket[lesson_id] = 1
                request.session['basket'] = basket
                discount_delta = discount_delta_zero(request)
                json_response = json.dumps({'item_added': 'True',
                                            'discount_delta': discount_delta,
                                            })
                return HttpResponse(json_response,
                                    content_type='application/json')
            # If lesson is in basket
            else:
                json_response = json.dumps({'item_added': 'already_added'})
                return HttpResponse(json_response,
                                    content_type='application/json')
        # If incorrect POST data
        else:
            json_response = json.dumps({'item_added': 'invalid_data'})
            return HttpResponse(json_response, content_type='application/json')
    # If not post request
    else:
        messages.error(request, ("Invalid request, please select lessons from "
                                 "the lessons page"))
        return redirect(reverse('home'))


@login_required
def remove_from_basket(request):
    """ Removes item from basket """
    basket = request.session.get('basket', {})

    if 'lesson_id' in request.POST:
        lesson_id = request.POST.get('lesson_id')
        if Lesson.objects.filter(lesson_id=lesson_id).exists():
            basket.pop(lesson_id)
            request.session['basket'] = basket
            json_response = json.dumps({'item_removed': 'True'})
            return HttpResponse(json_response,
                                content_type='application/json')

    messages.error(request, ("Invalid request, invalid lesson or bad "
                             " form data"))
    return redirect(reverse('view_basket'))
