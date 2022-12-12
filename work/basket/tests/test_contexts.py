from django.test import TestCase

from profiles.models import UserProfile
from lessons.models import Lesson


class TestBasketContexts(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def test_lesson_removed_while_in_customers_basket(self):
        '''
        If a lesson is removed while in a customers
        basket, it us removed by contexts
        '''
        # Add a lesson to basket
        customer = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=customer.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        lesson = Lesson.objects.get(lesson_name='B Lesson')
        lesson_name = lesson.lesson_name
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertContains(response, '"item_added": "True"')

        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, lesson.lesson_name)

        # Delete the actual lesson
        lesson.delete()
        self.assertFalse(
            Lesson.objects.filter(lesson_name='B Lesson').exists())

        # Go to basket, lesson is removed by basket.contexts.py
        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')

        self.assertNotContains(response, lesson_name)
