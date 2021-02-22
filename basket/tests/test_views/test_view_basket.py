from django.test import TestCase
from django.conf import settings

import html

from basket.contexts import basket_contents
from profiles.models import UserProfile
from lessons.models import Lesson
from checkout.models import OrderLineItem


class TestViewBasketViews(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

    def test_discount_met(self):
        '''
        View Basket with item in it.
        Discount is met and deducted from grand total
        banner and total shows discount is applied
        and discount is correctly applied
        '''
        # Remove all bought items
        OrderLineItem.objects.all().delete()

        # Check lesson is over discount threshold
        lesson = Lesson.objects.get(lesson_name='B Lesson')
        self.assertGreaterEqual(lesson.price, settings.DISCOUNT_THRESHOLD)

        # Add item to basket
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertContains(response, '"item_added": "True"')

        # View Basket page
        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')

        # Send request through context processor to get current grand total
        request = response.wsgi_request
        grand_total = round(basket_contents(request)['grand_total'], 2)
        # Calculate grand total
        test_grand_total = round(lesson.price - ((lesson.price / 100) *
                                 settings.DISCOUNT_PERCENTAGE), 2)
        # Do totals match
        self.assertEqual(grand_total, test_grand_total)

        # Lesson details and price appear on webpage
        self.assertContains(response, lesson.lesson_name)
        self.assertContains(response, html.escape(f'Total: €{lesson.price}'))
        self.assertContains(
            response,
            html.escape(f'Grand Total: €{grand_total}'))
        self.assertContains(
            response,
            f'{settings.DISCOUNT_PERCENTAGE}% discount applied!')

        # Discount banner threshold met
        self.assertContains(response,
                            (f'A {settings.DISCOUNT_PERCENTAGE}% discount has '
                             'been applied to your basket!'))

    def test_discount_not_met(self):
        '''
        View Basket with item in it.
        Discount is not met and not deducted from grand total
        amount more to spend for discount is displayed
        '''
        OrderLineItem.objects.all().delete()
        # Check lesson is under discount threshold
        lesson = Lesson.objects.get(lesson_name='Z Lesson')
        self.assertLess(lesson.price, settings.DISCOUNT_THRESHOLD)

        # Add item to basket
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertContains(response, '"item_added": "True"')
        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')

        # Lesson details and price
        self.assertContains(response, lesson.lesson_name)
        self.assertContains(response, html.escape(f'Total: €{lesson.price}'))
        self.assertContains(response,
                            html.escape(f'Grand Total: €{lesson.price}'))

        # Discount delta
        discount_delta = settings.DISCOUNT_THRESHOLD - lesson.price
        
        # View basket page
        self.assertContains(
            response, html.escape(f'Spend €{discount_delta} more for a '
                                  f'{settings.DISCOUNT_PERCENTAGE}% '
                                  'discount!'))

        # Discount percentage
        self.assertContains(
            response,
            html.escape(f'Get a {settings.DISCOUNT_PERCENTAGE}% discount '
                        'when you spend more than')
                        )

    def test_logged_out(self):
        ''' Logged out users will be redirect to login page '''
        self.client.logout()
        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/accounts/login/?next=/basket/')
        self.assertContains(response, ('If you have not created an account '
                                       'yet, then please'))

    def test_empty_basket(self):
        ''' Displays empty basket page '''
        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, ("Your basket is empty. Browse our "
                                       "instructors to find a lesson to "
                                       "suit you!"))
