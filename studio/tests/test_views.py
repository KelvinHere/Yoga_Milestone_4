from django.test import TestCase

import html

from lessons.models import Lesson
from checkout.models import OrderLineItem

class StudioViews(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.free_lesson = Lesson.objects.filter(is_free=True).first()
        self.paid_lesson = Lesson.objects.filter(is_free=False, lesson_name='Z Lesson').first()
        self.invalid_lesson_id = "SDFGGRFVAD"
        self.complete_user = {'username': 'complete_user',
                              'password': 'orange99'}
        self.incomplete_user = {'username': 'incomplete_user',
                                'password': 'orange99'}

    def test_studio_page_logged_out(self):
        # Logged out users will be redirected to login page
        response = self.client.get(f'/studio/{self.free_lesson.lesson_id}/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next=/studio/{self.free_lesson.lesson_id}/')
        self.assertContains(response, 'If you have not created an account yet, then please')

    def test_studio_page_invalid_lesson(self):
        # Passed an invalid lesson, view will send user home
        login_successful = self.client.login(username=self.complete_user['username'],
                                             password=self.complete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.get(f'/studio/{self.invalid_lesson_id}/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, 'Invalid lesson')

    def test_studio_page_free_lesson(self):
        # Logged in users can access free lessons
        login_successful = self.client.login(username=self.complete_user['username'],
                                             password=self.complete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.get(f'/studio/{self.free_lesson.lesson_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/studio.html')
        self.assertContains(response, self.free_lesson.lesson_name)
        self.assertContains(response, self.free_lesson.description)

    def test_studio_page_paid_lesson_not_purchased(self):
        # Users cannot access lessons they have not paid for that are not free
        login_successful = self.client.login(username=self.incomplete_user['username'],
                                             password=self.incomplete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.get(f'/studio/{self.paid_lesson.lesson_id}/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, 'You do not own this lesson.')

    def test_studio_page_paid_lesson_is_purchased(self):
        # Users can access lessons they paid for
        login_successful = self.client.login(username=self.complete_user['username'],
                                             password=self.complete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.get(f'/studio/{self.paid_lesson.lesson_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/studio.html')
        self.assertContains(response, self.paid_lesson.lesson_name)
        self.assertContains(response, html.escape(self.paid_lesson.description))
