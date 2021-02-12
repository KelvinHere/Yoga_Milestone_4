from django.test import TestCase
from django.shortcuts import reverse

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

    # Lessons View
    def test_get_lessons(self):
        # Renders a list of all lessons
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        self.assertContains(response, 'All Lessons')

    # Lesson Page with instructor filter
    def test_lessons_with_valid_instructor_filter(self):
        # Displays the instructors profile and all their
        # lessons underneath
        response = self.client.get(f'/lessons/', {'instructor': self.instructor.id}, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        self.assertContains(response, self.instructor.user.username)
        self.assertContains(response, html.escape(self.instructor.profile_description))

    # Subscription View
    def test_subscriptions_logged_out(self):
        # Logged out users will be redirect to login page
        response = self.client.get(f'/lessons/subscriptions/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next=/lessons/subscriptions/')
        self.assertContains(response, html.escape('If you have not created an account yet, then please'))

    def test_subscibe_to_lesson(self):
        # Successful subscription creates a new Subscription object
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=self.complete_user['username'],
                                             password=self.complete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.get('/lessons/subscriptions/', {'subscribe': 'true', 'lesson_id': self.free_lesson.lesson_id}, follow=True)
        self.assertTrue(Subscription.objects.filter(lesson=self.free_lesson, user=profile).exists())

    def test_subscribe_to_lesson_invalid_lesson(self):
        # Invalid lesson passed to subscribe will return user to
        # lessons page with error message
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=self.complete_user['username'],
                                             password=self.complete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.get('/lessons/subscriptions/', {'subscribe': 'true', 'lesson_id': self.invalid_lesson_id}, follow=True)
        self.assertFalse(Subscription.objects.filter(lesson=self.free_lesson, user=profile).exists())
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response,
                             expected_url=reverse('lessons'),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(
            response,
            'Invalid request, no lessons have been subscribed')

    def test_subscribe_to_lesson_invalid_subscribe_request(self):
        # Invalid subscribe argument passed to subscribe will
        # return user to lessons page with error message
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=self.complete_user['username'],
                                             password=self.complete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.get('/lessons/subscriptions/', {'subscribe': 'oops', 'lesson_id': self.invalid_lesson_id}, follow=True)
        self.assertFalse(Subscription.objects.filter(lesson=self.free_lesson, user=profile).exists())
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response,
                             expected_url=reverse('lessons'),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(
            response,
            'Invalid request, no lessons have been subscribed')

    def test_subscribe_to_lesson_post_request(self):
        # Post request will return user to 
        # lessons page with error message
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=self.complete_user['username'],
                                             password=self.complete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.post('/lessons/subscriptions/', {'subscribe': 'test', 'lesson_id': self.invalid_lesson_id}, follow=True)
        self.assertFalse(Subscription.objects.filter(lesson=self.free_lesson, user=profile).exists())
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response,
                             expected_url=reverse('lessons'),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(
            response,
            'Invalid request, no lessons have been subscribed')

    def test_unsubscribe_to_lesson_valid_request(self):
        # Valid request will remove the subscription
        # object for this user / lesson
        login_successful = self.client.login(username=self.incomplete_user['username'],
                                             password=self.incomplete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.get('/lessons/subscriptions/', {'subscribe': 'false', 'lesson_id': self.subscribed_lesson.lesson_id}, follow=True)
        self.assertFalse(Subscription.objects.filter(lesson=self.subscribed_lesson, user=self.subscribed_user).exists())

    # Instructor_admin View
    def test_instructor_admin_logged_out(self):
        # Logged out users will be redirect to login page
        response = self.client.get(f'/lessons/instructor_admin/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next=/lessons/instructor_admin/')
        self.assertContains(response, html.escape('If you have not created an account yet, then please'))


    def test_instructor_admin_not_instructor(self):
        # A non instructor will be redirected home with an error message
        login_successful = self.client.login(username=self.complete_user['username'],
                                             password=self.complete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/instructor_admin/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, 'Only instructors can do this.')

    def test_instructor_admin_as_instructor(self):
        # Instructors can view this page and see lessons / sales
        login_successful = self.client.login(username=self.instructor_credentials['username'],
                                             password=self.instructor_credentials['password'])
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/instructor_admin/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/instructor_admin.html')
        self.assertContains(response, 'Lesson Admin for instructor_2')
        # Contains instructors lessons
        self.assertContains(response, html.escape("Instructor 2's first lesson"))
        # Contains instructors sales
        self.assertContains(response, html.escape("24.99 - 30%"))
