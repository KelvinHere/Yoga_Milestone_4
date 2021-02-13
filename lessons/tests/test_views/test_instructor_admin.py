from django.test import TestCase

import html

from profiles.models import UserProfile
from lessons.models import Subscription, Lesson


class TestInstructorAdminView(TestCase):
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

    def test_logged_out(self):
        '''
        Logged out users will be redirect to login page
        '''
        response = self.client.get('/lessons/instructor_admin/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next=/lessons/instructor_admin/')
        self.assertContains(response, 'If you have not created an account yet, then please')

    def test_not_instructor(self):
        '''
        A non instructor will be redirected home with an error message
        '''
        login_successful = self.client.login(username=self.complete_user['username'],
                                             password=self.complete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.get('/lessons/instructor_admin/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, 'Only instructors can do this.')

    def test_is_an_instructor(self):
        '''
        Instructors can view this page and see lessons / sales
        '''
        login_successful = self.client.login(username=self.instructor_credentials['username'],
                                             password=self.instructor_credentials['password'])
        self.assertTrue(login_successful)
        response = self.client.get('/lessons/instructor_admin/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/instructor_admin.html')
        self.assertContains(response, 'Lesson Admin for instructor_2')
        # Contains instructors lessons
        self.assertContains(response, html.escape("Instructor 2's first lesson"))
        # Contains instructors sales
        self.assertContains(response, html.escape("24.99 - 30%"))
