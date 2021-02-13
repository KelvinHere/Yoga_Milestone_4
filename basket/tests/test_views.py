from django.test import TestCase

import html

from profiles.models import UserProfile
from lessons.models import Subscription, Lesson
from checkout.models import OrderLineItem


class TestBasketViews(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

    def test_logged_out(self):
        ''' Logged out users will be redirect to login page '''
        self.client.logout()
        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/accounts/login/?next=/basket/')
        self.assertContains(response, 'If you have not created an account yet, then please')

    def test_empty_basket_page(self):
        ''' Displays empty basket page '''
        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, 'Your basket is empty. Browse our instructors to find a lesson to suit you!')

    def test_add_free_lesson_to_basket(self):
        '''
        Free item added returns invalid_item_is free
        in json response, item not added to basket
        '''
        lesson = Lesson.objects.get(lesson_name='H Lesson')
        response = self.client.post('/basket/add_to_basket/', {'lesson_id': lesson.lesson_id}, follow=True)
        self.assertContains(response, '"item_added": "invalid_item_is_free"')

        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertNotContains(response, 'H Lesson')

    def test_add_to_basket_valid_item(self):
        ''' Add item not owned to basket then show in basket '''
        lesson = Lesson.objects.get(lesson_name='B Lesson')
        response = self.client.post('/basket/add_to_basket/', {'lesson_id': lesson.lesson_id}, follow=True)
        self.assertContains(response, '"item_added": "True"')

        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, 'B Lesson')

    def test_invalid_item(self):
        '''
        invalid item returns json response
        '''
        response = self.client.post('/basket/add_to_basket/', {'lesson_id': 'INVALID_ID'}, follow=True)
        self.assertContains(response, '"item_added": "invalid_item"')

    def test_invalid_post_data(self):
        '''
        invalid post data returns json response
        '''
        response = self.client.post('/basket/add_to_basket/', {'INVALID_POST_DATA': 'INVALID_ID'}, follow=True)
        self.assertContains(response, '"item_added": "invalid_data"')

    def test_adding_already_purchased_lesson(self):
        '''
        adding an already purchased lesson
        returns json response
        '''
        lesson = Lesson.objects.get(lesson_name='Z Lesson')
        response = self.client.post('/basket/add_to_basket/', {'lesson_id': lesson.lesson_id}, follow=True)
        self.assertContains(response, '"item_added": "already_owned"')

    def test_adding_lesson_that_is_already_added(self):
        '''
        adding an already added lesson
        returns json response
        '''
        lesson = Lesson.objects.get(lesson_name='B Lesson')
        response = self.client.post('/basket/add_to_basket/', {'lesson_id': lesson.lesson_id}, follow=True)
        self.assertContains(response, '"item_added": "True"')
        response = self.client.post('/basket/add_to_basket/', {'lesson_id': lesson.lesson_id}, follow=True)
        self.assertContains(response, '"item_added": "already_added"')

        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, 'B Lesson')
        html_str = response.content.decode("utf-8")
        # Only contains one of this item in basket
        self.assertEqual(html_str.count(f'id="row_for_{lesson.lesson_id}'), 1)

    def test_discount_not_met(self):
        '''
        Discount is not met and not deducted from grand total
        amount more to spend for discount is displayed
        '''
        basket = self.client.session['basket']
        

        OrderLineItem.objects.all().delete()
        lesson = Lesson.objects.get(lesson_name='Z Lesson')
        response = self.client.post('/basket/add_to_basket/', {'lesson_id': lesson.lesson_id}, follow=True)
        self.assertContains(response, '"item_added": "True"')
        
        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, 'Z Lesson')
        self.assertContains(response, html.escape(f'Total: €{lesson.price}'))
        self.assertContains(response, html.escape(f'Grand Total: €{lesson.price}'))
        self.assertContains(response, html.escape('more for a 10% discount!'))
        # Discount banner, threshold not met
        self.assertContains(response, html.escape('Get a 10% discount when you spend more than'))

    def test_discount_met(self):
        '''
        Discount is  met and deducted from grand total
        banner and total shows discount is applied
        '''
        OrderLineItem.objects.all().delete()
        lesson = Lesson.objects.get(lesson_name='B Lesson')
        response = self.client.post('/basket/add_to_basket/', {'lesson_id': lesson.lesson_id}, follow=True)
        self.assertContains(response, '"item_added": "True"')

        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        print(response.content.decode("utf-8"))
        self.assertContains(response, 'B Lesson')
        self.assertContains(response, html.escape(f'Total: €{lesson.price}'))
        self.assertLess(response, '))
        self.assertContains(response, 'discount applied!')
        # Discount banner threshold met
        self.assertContains(response, 'A 10% discount has been applied to your basket!')


