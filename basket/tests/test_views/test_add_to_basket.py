from django.test import TestCase

from profiles.models import UserProfile
from lessons.models import Lesson


class TestAddToBasketView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

    def test_add_free_lesson(self):
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

    def test_add_valid_item(self):
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

    def test_add_invalid_item(self):
        '''
        invalid item returns json response
        '''
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': 'INVALID_ID'},
                                    follow=True)
        self.assertContains(response, '"item_added": "invalid_item"')

    def test_add_invalid_post_data(self):
        '''
        invalid post data returns json response
        '''
        response = self.client.post('/basket/add_to_basket/',
                                    {'INVALID_POST_DATA': 'INVALID_ID'},
                                    follow=True)
        self.assertContains(response, '"item_added": "invalid_data"')

    def test_add_already_purchased_lesson(self):
        '''
        adding an already purchased lesson
        returns json response
        '''
        lesson = Lesson.objects.get(lesson_name='Z Lesson')
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertContains(response, '"item_added": "already_owned"')

    def test_add_lesson_that_is_already_in_basket(self):
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
