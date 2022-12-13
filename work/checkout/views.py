from django.shortcuts import (render,
                              redirect,
                              reverse,
                              get_object_or_404,
                              HttpResponse)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from basket.contexts import basket_contents
from .models import Order, OrderLineItem
from lessons.models import Lesson
from profiles.models import UserProfile

import stripe
import json


@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        basket = request.session.get('basket', {})
        order_form = OrderForm(request.POST)

        # Confirm with stripe this order has been paid for
        try:
            payment_intent_id = (request.POST.get('client_secret')
                                 .split('_secret')[0])
            stripe.api_key = settings.STRIPE_SECRET_KEY
            fetched_intent = stripe.PaymentIntent.retrieve(payment_intent_id, )
            paid = fetched_intent['charges']['data'][0]['paid']
        except Exception:
            messages.error(request, ("Error:  Could not confirm order with "
                                     "stripe no charges have been made."))
            return redirect(reverse('view_basket'))

        # Create order if form is valid and has been paid for
        if order_form.is_valid() and paid:
            order = order_form.save(commit=False)
            payment_intent_id = (request.POST.get('client_secret')
                                             .split('_secret')[0])
            order.stripe_id = payment_intent_id
            order.original_basket = json.dumps(basket)
            order.profile = profile
            order.save()
            for item in basket.items():
                lesson = get_object_or_404(Lesson, lesson_id=item[0])
                order_line_item = OrderLineItem(
                    order=order,
                    lesson=lesson,
                    profile=profile,)
                order_line_item.save()
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        else:
            messages.error(request, ("There was an error with your form, no "
                                     "charges have been made."))
            return redirect(reverse('checkout'))

    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "Your basket is empty")
            return redirect(reverse('home'))

        # Prepare grand total for stripe and create payment intent
        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY)

        # Get full name
        full_name = ''
        if profile.first_name and profile.last_name:
            full_name = f'{profile.first_name} {profile.last_name}'

        order_form = OrderForm(initial={'full_name': full_name,
                                        'email': profile.user.email})

    if not stripe_public_key:
        messages.warning(request, 'Missing public key for stripe')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


@login_required
def checkout_success(request, order_number):
    """ Handle successful checkouts """
    try:
        order = get_object_or_404(Order, order_number=order_number)
    except Exception:
        messages.error(request, ('This order was not found, please contact '
                                 f'{settings.DEFAULT_FROM_EMAIL} for support'))
        return redirect(reverse('home'))

    profile = get_object_or_404(UserProfile, user=request.user)
    if profile != order.profile:
        messages.error(request, ('This order does not belong to this account, '
                                 'if this is an misake please contact '
                                 f'{settings.DEFAULT_FROM_EMAIL} for '
                                 'support.'))
        return redirect(reverse('home'))

    messages.success(request, f'Order successfully processed! \
                                Order number : {order_number} \
                                An email has been sent to {order.email}.')

    if 'basket' in request.session:
        del request.session['basket']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order
    }

    return render(request, template, context)


@require_POST
@login_required
def attach_basket_to_intent(request):
    try:
        payment_intent_id = (request.POST.get('client_secret')
                                         .split('_secret')[0])
        # Setup stripe with secret key so payment intent can be modified
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(payment_intent_id, metadata={
            'user': request.user,
            'basket': json.dumps(request.session.get('basket', {})),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be processed. '
                                 'please try again later.  You have NOT been '
                                 'charged for this transaction.'
                                 f' Error: {e}'))
        return HttpResponse(content=e, status=400)
