from django.test import TestCase
from django.shortcuts import reverse
from django.conf import settings

import html

from basket.contexts import basket_contents
from profiles.models import UserProfile
from lessons.models import Lesson
from checkout.models import OrderLineItem


class TestBasketViews(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

    def test_discount_met(self):
        '''
        Discount is  met and deducted from grand total
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

    def test_empty_basket_page(self):
        ''' Displays empty basket page '''
        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, ("Your basket is empty. Browse our "
                                       "instructors to find a lesson to "
                                       "suit you!"))

    def test_add_free_lesson_to_basket(self):
        '''
        Free item added returns invalid_item_is free
        in json response, item not added to basket
        '''
        lesson = Lesson.objects.get(lesson_name='H Lesson')
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertContains(response, '"item_added": "invalid_item_is_free"')

        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertNotContains(response, lesson.lesson_name)

    def test_add_to_basket_valid_item(self):
        ''' Add item not owned to basket then show in basket '''
        lesson = Lesson.objects.get(lesson_name='B Lesson')
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertContains(response, '"item_added": "True"')

        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, lesson.lesson_name)

    def test_invalid_item(self):
        '''
        invalid item returns json response
        '''
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': 'INVALID_ID'},
                                    follow=True)
        self.assertContains(response, '"item_added": "invalid_item"')

    def test_invalid_post_data(self):
        '''
        invalid post data returns json response
        '''
        response = self.client.post('/basket/add_to_basket/',
                                    {'INVALID_POST_DATA': 'INVALID_ID'},
                                    follow=True)
        self.assertContains(response, '"item_added": "invalid_data"')

    def test_adding_already_purchased_lesson(self):
        '''
        adding an already purchased lesson
        returns json response
        '''
        lesson = Lesson.objects.get(lesson_name='Z Lesson')
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertContains(response, '"item_added": "already_owned"')

    def test_adding_lesson_that_is_already_added(self):
        '''
        adding an already added lesson
        returns json response
        '''
        lesson = Lesson.objects.get(lesson_name='B Lesson')
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertContains(response, '"item_added": "True"')

        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertContains(response, '"item_added": "already_added"')

        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, lesson.lesson_name)
        html_str = response.content.decode("utf-8")
        # Only contains one of this item in basket
        self.assertEqual(html_str.count(f'id="row_for_{lesson.lesson_id}'), 1)

    def test_remove_from_basket_valid_request(self):
        '''
        Removes an item from the basket
        '''
        OrderLineItem.objects.all().delete()
        lesson = Lesson.objects.get(lesson_name='B Lesson')

        # Add item to basket and check it is there
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '"item_added": "True"')

        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, lesson.lesson_name)

        # Remove item from basket and check it has gone
        response = self.client.post('/basket/remove_from_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '"item_removed": "True"')

        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertNotContains(response, lesson.lesson_name)

    def test_remove_from_basket_invalid_lessonid(self):
        '''
        Invalid item redirects user to basket with error message
        '''
        response = self.client.post('/basket/remove_from_basket/',
                                    {'lesson_id': 'INVALID_LESSON_ID'},
                                    follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('view_basket'),
                             status_code=302,
                             target_status_code=200)

    def test_remove_from_basket_invalid_post_data(self):
        '''
        Invalid post data item redirects user
        to basket with error message
        '''
        response = self.client.post('/basket/remove_from_basket/',
                                    {'INVALID_POST': 'A'},
                                    follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('view_basket'),
                             status_code=302,
                             target_status_code=200)
