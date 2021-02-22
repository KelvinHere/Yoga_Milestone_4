from django.test import TestCase
from django.shortcuts import reverse
from django.conf import settings

from checkout.models import OrderLineItem, Order
from profiles.models import UserProfile
from lessons.models import Lesson

import re


class TestCheckoutViews(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        # Login
        self.profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(
            username=self.profile.user.username,
            password='orange99')
        self.assertTrue(login_successful)

    # Checkout Page
    def test_checkout_logged_out(self):
        '''
        Logged out users will be redirected to login page
        '''
        self.client.logout()
        response = self.client.get('/checkout/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/accounts/login/?next=/checkout/')
        self.assertContains(response, ('If you have not created an account '
                                       'yet, then please'))

    def test_checkout_valid_request(self):
        '''
        Checkout GET request takes user to checkout page
        '''
        # Remove previous purchases
        Order.objects.all().delete()

        # Add items
        lesson = Lesson.objects.get(lesson_name='B Lesson')
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertTrue(response.status_code, 200)

        lesson = Lesson.objects.get(lesson_name='Z Lesson')
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertTrue(response.status_code, 200)

        # Check basket has both items
        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, 'B Lesson')
        self.assertContains(response, 'Z Lesson')

        # Checkout
        response = self.client.get('/checkout/')
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertContains(response, 'For 2 items')

    def test_checkout_empty_basket(self):
        '''
        Checkout page with empty basket redirects
        user home with error message
        '''
        response = self.client.get('/checkout/', follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('home'),
                             status_code=302,
                             target_status_code=200)
        self.assertTemplateUsed(response, 'home/index.html')

    # Checkout success page
    def test_checkout_success(self):
        '''
        Order successfully placed check all items
        are displayed on checkout success page
        '''
        order = Order.objects.filter().first()
        items_in_order = OrderLineItem.objects.filter(order=order)

        response = self.client.get(
            f'/checkout/checkout_success/{order.order_number}')
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, ('Your order was successfully placed, '
                                       'below is your order information'))

        # All lessons pruchased are included in page
        for item in items_in_order:
            self.assertContains(response, item.lesson.lesson_name)

    def test_checkout_success_invalid_order_number(self):
        '''
        Invalid order number for checkout success page
        redirects user home with error message
        '''
        response = self.client.get(
            '/checkout/checkout_success/INVALID_ORDER_NUMBER',
            follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('home'),
                             status_code=302,
                             target_status_code=200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response,
                            ('This order was not found, please contact '
                             f'{settings.DEFAULT_FROM_EMAIL} for support'))

    def test_checkout_success_not_correct_profile(self):
        '''
        Accessing an order number that does not belong
        to logged in user on checkout success page, redirects
        user home with error message
        '''
        # Login as incomplete user
        self.client.logout()
        login_successful = self.client.login(username='incomplete_user',
                                             password='orange99')
        self.assertTrue(login_successful)

        # Get complete users order
        order = Order.objects.filter(
            profile__user__username='complete_user').first()

        response = self.client.get(
            f'/checkout/checkout_success/{order.order_number}',
            follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('home'),
                             status_code=302,
                             target_status_code=200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, ('This order does not belong to this '
                                       'account'))

    def test_checkout_valid_post(self):
        '''
        Submitting a valid checkout form will carry out
        the order process then redirect the user to the
        checkout success page with success message
        '''
        # Remove all purchases
        Order.objects.all().delete()

        # Add items
        lesson = Lesson.objects.get(lesson_name='B Lesson')
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertTrue(response.status_code, 200)

        # Check basket has item
        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, 'B Lesson')

        # Checkout
        response = self.client.get('/checkout/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertContains(response, 'For 1 item')

        # Get client secret from rendered page
        client_secret = re.search(
            r'id_client_secret" type="application\/json">"(.+?_secret).+',
            response.content.decode("utf-8")
            )[1]

        # Response redirects to checkout success and order is created
        response = self.client.post('/checkout/',
                                    {'full_name': 'CompleteUser',
                                     'email': 'complete_user@test.com',
                                     'client_secret': client_secret, },
                                    follow=True)

        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertContains(response, 'B Lesson')
        self.assertContains(response, ('Your order was successfully placed, '
                                       'below is your order information'))
        self.assertTrue(Order.objects.filter(profile=self.profile).exists())

    def test_checkout_invalid_post(self):
        '''
        Submitting an invalid checkout form returns
        user to checkout with error message
        '''
        # Remove all purchases
        Order.objects.all().delete()

        # Add items
        lesson = Lesson.objects.get(lesson_name='B Lesson')
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertTrue(response.status_code, 200)

        # Checkout
        response = self.client.get('/checkout/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertContains(response, 'For 1 item')

        # Response redirects to checkout with error message
        response = self.client.post('/checkout/',
                                    {'full_name': 'CompleteUser',
                                     'WRONG_FIELD': 'complete_user@test.com',
                                     'client_secret': 'INVALID_SECRET', },
                                    follow=True)

        print(response.content.decode("UTF-8"))

        self.assertRedirects(response,
                             expected_url=reverse('checkout'),
                             status_code=302,
                             target_status_code=200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

        self.assertContains(response, 'For 1 item')
        self.assertContains(response, ("There was an error with your form, no "
                                       "charges have been made."))
        self.assertFalse(Order.objects.filter(profile=self.profile).exists())
