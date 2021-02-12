from django.test import TestCase

import html

from profiles.models import UserProfile
from lessons.models import Subscription, Lesson


class TestSubscriptionView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.instructor = UserProfile.objects.filter(is_instructor=True).first()
        self.free_lesson = Lesson.objects.filter(is_free=True).first()
        self.paid_lesson = Lesson.objects.filter(is_free=False, lesson_name='Z Lesson').first()
        self.invalid_lesson_id = "SDFGGRFVAD"
        self.subscribed_user = UserProfile.objects.get(id=5)  # = incomplete_user
        self.subscribed_lesson = Lesson.objects.get(id=2)
        self.subscription = Subscription.objects.get(lesson=self.subscribed_lesson,
                                                     user=self.subscribed_user)
        self.complete_user = {'username': 'complete_user',
                              'password': 'orange99'}
        self.incomplete_user = {'username': 'incomplete_user',
                                'password': 'orange99'}
        self.instructor_credentials = {'username': 'instructor_2',
                                       'password': 'orange99'}

    def test_get_lessons(self):
        '''
        Renders a list of all lessons
        '''
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        self.assertContains(response, 'All Lessons')

    def test_lessons_with_valid_instructor_filter(self):
        '''
        Displays the instructors profile and all their
        lessons underneath
        '''
        response = self.client.get('/lessons/', {'instructor': self.instructor.id}, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        self.assertContains(response, self.instructor.user.username)
        self.assertContains(response, html.escape(self.instructor.profile_description))

   