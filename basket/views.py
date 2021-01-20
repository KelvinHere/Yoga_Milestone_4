from django.shortcuts import render, HttpResponse
import json


def view_basket(request):
    """ A view to view the basket """
    template = 'basket/basket.html'
    return render(request, template)


def add_to_basket(request):
    """ Add a lesson to the basket """
    basket = request.session.get('basket', {})

    if request.method == 'POST':
        if 'lesson_id' in request.POST:
            lesson_id = request.POST.get('lesson_id')
            if lesson_id not in list(basket.keys()):
                basket[lesson_id] = 1
                request.session['basket'] = basket
                json_response = json.dumps({'item_added': 'True'})
                return HttpResponse(json_response, content_type='application/json')
            else:
                json_response = json.dumps({'item_added': 'already_added'})
                return HttpResponse(json_response, content_type='application/json')
        else:
            return HttpResponse('Error: No lesson_id in POST', status=500)
    else:
        return HttpResponse('Error: Not POST', status=500)


def remove_from_basket(request):
    """ Removes item from basket """
    basket = request.session.get('basket', {})

    if request.method == 'POST':
        if 'lesson_id' in request.POST:
            lesson_id = request.POST.get('lesson_id')
            basket.pop(lesson_id)
            request.session['basket'] = basket
            json_response = json.dumps({'item_removed': 'True'})
            return HttpResponse(json_response, content_type='application/json')
        else:
            return HttpResponse('Error: No lesson_id in POST', status=500)
    else:
        return HttpResponse('Error: Not POST', status=500)
