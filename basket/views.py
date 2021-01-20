from django.shortcuts import render

def view_basket(request):
    """ A view to view the basket """

    return render(request, 'basket/basket.html')