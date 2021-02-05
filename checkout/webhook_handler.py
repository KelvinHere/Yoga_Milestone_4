from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from checkout.models import Order, OrderLineItem
from lessons.models import Lesson
from profiles.models import UserProfile

import json
import time


class StripeWH_Handler:
    """ Handle Stripe Webhooks """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """
        Send confirmation email on successful order
        """
        customer_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL, }
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email],
        )

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

        billing_details = intent.charges.data[0].billing_details
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    stripe_id=payment_intent_id,
                    original_basket=basket,)
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: \
                              Order already in database',
                    status=200
                    )
        else:
            order = None
            try:
                user = get_object_or_404(User, username=username)
                profile = get_object_or_404(UserProfile, user=user)
                order = Order.objects.create(
                    profile=profile,
                    stripe_id=payment_intent_id,
                    original_basket=basket,
                    full_name=intent.charges.data[0]['billing_details']['name'],
                    email=intent.charges.data[0]['billing_details']['email'],
                )
                for lesson_id, value in json.loads(basket).items():
                    lesson = get_object_or_404(Lesson, lesson_id=lesson_id)
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
                    content=f'Webhook received: {event["type"]} | \
                                Error: {e}',
                    status=500
                    )
        self._send_confirmation_email(order)
        return HttpResponse(
                        content=f'Webhook received: {event["type"]} | \
                                  Success: Created order in webhook',
                        status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle payment_intent.failed webhook
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
