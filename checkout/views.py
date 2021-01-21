from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from basket.contexts import basket_contents
from .models import Order, OrderLineItem
from lessons.models import Lesson
from profiles.models import UserProfile

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        basket = request.session.get('basket', {})
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.profile = profile
            order.save()
            for item in basket.items():
                lesson = get_object_or_404(Lesson, lesson_id=item[0])
                try:
                    order_line_item = OrderLineItem(
                        order=order,
                        lesson=lesson,
                        profile=profile,
                    )
                    order_line_item.save()
                except Lesson.DoesNotExist:
                    messages.error(request, "One of the lessons was not found please contact us for assistance")
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form.')

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

def checkout_success(request, order_number):
    """ Handle successful checkouts """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order number successfully processed! \
        Order number : {order_number} \
        An email has been sent to {order.email}.')

    if 'basket' in request.session:
        del request.session['basket']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order
    }

    return render(request, template, context)
