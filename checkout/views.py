from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from basket.contexts import basket_contents
from .models import Order, OrderLineItem
from lessons.models import Lesson

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        basket = request.session.get('basket', {})
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_form.save()
            for item in basket.items():
                try:
                    lesson = Lesson.objects.get(lesson_id=item.lesson.lesson_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        lesson=lesson,

                    )
                except:
                    print('a')
    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "Your basket is empty")
            return redirect(reverse('index'))

        #Prepare grand total for stripe and create payment intent
        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY
        )
    
        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Missing public key for stripe')
    
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)