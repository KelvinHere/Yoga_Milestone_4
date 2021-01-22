from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from checkout.models import Order, OrderLineItem
from lessons.models import Lesson
from profiles.models import UserProfile

import json
import time


class StripeWH_Handler:
    """ Handle Stripe Webhooks """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle generic/unknown/unexpected webhook events
        """
        return HttpResponse(
            content=f'Unhandled Webhook received!: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle payment_intent.succeeded webhook
        """
        intent = event.data.object
        payment_intent_id = intent.id
        basket = intent.metadata.basket
        username = intent.metadata.user
        print('#Username')
        print(username)
        print('#basket')
        print(basket)

        billing_details = intent.charges.data[0].billing_details
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                print('#Try to find order')
                print(payment_intent_id)
                print(basket)
                order = Order.objects.get(
                    stripe_id=payment_intent_id,
                    original_basket=basket,)
                order_exists = True
                break
            except Order.DoesNotExist:
                print('#order not found')
                attempt += 1
                print(f'Attempt {attempt}')
                time.sleep(1)
        if order_exists:
            print('#Order found')
            return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Order already in database',
                    status=200)
        else:
            print('#Order was not found after 5 attempts')
            order = None
            try:
                print('#Trying to create order')
                order = Order.objects.create(
)
                print('#Trying to get user')
                user = get_object_or_404(User, username=username)
                print('#user')
                print(user)
                profile = get_object_or_404(UserProfile, user=user)
                print('#Profile')
                print(profile)
                for item in json.loads(basket):
                    lesson = get_object_or_404(Lesson, lesson_id=item[0])
                    order_line_item = OrderLineItem(
                        order=order,
                        lesson=lesson,
                        profile=profile,
                    )
                    order_line_item.save()
            except Exception as e:
                    if order:
                        order.delete()
                    return HttpResponse(
                        content=f'Webhook received: {event["type"]} | Error: {e}',
                        status=500)
        return HttpResponse(
                        content=f'Webhook received: {event["type"]} | Success: Created order in webhook',
                        status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle payment_intent.failed webhook
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )