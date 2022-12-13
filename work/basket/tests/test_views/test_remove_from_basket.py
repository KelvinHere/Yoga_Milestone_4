from django.test import TestCase
from django.shortcuts import reverse

from profiles.models import UserProfile
from lessons.models import Lesson
from checkout.models import OrderLineItem


class TestRemoveFromBasketView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

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
