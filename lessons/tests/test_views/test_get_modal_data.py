from django.test import TestCase
from django.shortcuts import reverse

import html

from profiles.models import UserProfile
from lessons.models import Lesson


class TestGetModalData(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        # Get a review
        self.lesson = Lesson.objects.filter().first()
        # Login as normal user and create flag on that review
        self.flagger_profile = UserProfile.objects.get(user__username='incomplete_user')
        login_successful = self.client.login(username=self.flagger_profile.user.username,
                                             password='orange99')

    def test_get_modal_data(self):
        ''' Returns lesson information in json format '''
        response = self.client.post(
            '/lessons/get_modal_data/',
            data={'lesson_id': self.lesson.lesson_id})
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, self.lesson.lesson_name)
        self.assertContains(response, self.lesson.description)

    def test_invalid_lessonid(self):
        ''' Invalid lesson id returns error message '''
        response = self.client.post(
            '/lessons/get_modal_data/',
            data={'lesson_id': 'INVALID_ID'})
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '"status": "invalid_lesson"')

    def test_invalid_post_data(self):
        ''' Invalid post data returns error message '''
        response = self.client.post(
            '/lessons/get_modal_data/',
            data={'INVALID_POST_DATA': 'INVALID_DATA'})
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '"status": "invalid_request"')

    def test_get_modal_data_invalid_get_request(self):
        ''' Only POST requests are accepted '''
        response = self.client.get('/lessons/get_modal_data/', follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('home'),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(
            response,
            'You cannot perform this action')


