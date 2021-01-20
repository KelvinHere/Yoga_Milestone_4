from django.shortcuts import render

def view_basket(request):
    """ A view to view the basket """

    template = 'basket/basket.html'

    return render(request, template)

def add_to_basket(request, lesson_id):
    """ Add a lesson to the basket """

    # Create session for basket so user can browse site without losing basket contents
    basket = request.session.get('basket', {})

    if lesson_id not in list(basket.keys()):
        basket[lesson_id] = 1

    request.session['basket'] = basket

    template = "home/index.html"
    context = {
    }

    return render(request, template, context)