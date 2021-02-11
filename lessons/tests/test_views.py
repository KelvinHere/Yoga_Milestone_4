from django.test import TestCase

import html
import json

from profiles.models import UserProfile
from lessons.models import Subscription, Lesson

class TestLessonViews(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.instructor = UserProfile.objects.filter(is_instructor=True).first()
        self.free_lesson = Lesson.objects.filter(is_free=True).first()
        self.paid_lesson = Lesson.objects.filter(is_free=False, lesson_name='Z Lesson').first()
        self.invalid_lesson_id = "SDFGGRFVAD"
        self.complete_user = {'username': 'complete_user',
                              'password': 'orange99'}
        self.incomplete_user = {'username': 'incomplete_user',
                                'password': 'orange99'}

    def test_get_lessons(self):
        # Renders a list of all lessons
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        self.assertContains(response, 'All Lessons')

    def test_lessons_with_valid_instructor_filter(self):
        # Displays the instructors profile and all their
        # lessons underneath
        response = self.client.get(f'/lessons/', {'instructor': self.instructor.id}, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        self.assertContains(response, self.instructor.user.username)
        self.assertContains(response, html.escape(self.instructor.profile_description))

    def test_subscriptions_logged_out(self):
        # Logged out users will be redirect to login page
        response = self.client.get(f'/lessons/subscriptions/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next=/lessons/subscriptions/')
        self.assertContains(response, html.escape('If you have not created an account yet, then please'))

    def test_subscibe_to_lesson(self):
        login_successful = self.client.login(username=self.complete_user['username'],
                                             password=self.complete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.post('/lessons/subscriptions/', {'subscribe': 'true', 'lesson_id': self.free_lesson.lesson_id}, follow=True)
        print(response.content)
        #self.assertContains(response, 'subscribed')
        #self.assertTrue(Subscription.objects.filter(lesson=self.free_lesson.lesson_id, user=self.complete_user))

