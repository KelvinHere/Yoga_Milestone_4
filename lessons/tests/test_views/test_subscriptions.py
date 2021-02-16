from django.test import TestCase
from django.shortcuts import reverse

from profiles.models import UserProfile
from lessons.models import Subscription, Lesson


class TestSubscriptionView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.instructor = UserProfile.objects.filter(
            is_instructor=True).first()
        self.free_lesson = Lesson.objects.filter(
            is_free=True,
            lesson_name='H Lesson').first()
        self.paid_lesson = Lesson.objects.filter(
            is_free=False, lesson_name='Z Lesson').first()
        self.invalid_lesson_id = "SDFGGRFVAD"
        # subscribed user is incomplete_user
        self.subscribed_user = UserProfile.objects.get(id=5)
        self.subscribed_lesson = Lesson.objects.get(id=2)
        self.subscription = Subscription.objects.get(
            lesson=self.subscribed_lesson,
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
        response = self.client.get('/lessons/subscriptions/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response,
                             '/accounts/login/?next=/lessons/subscriptions/')
        self.assertContains(response, ('If you have not created an account '
                                       'yet, then please'))

    def test_subscibe_to_lesson(self):
        '''
        Successful subscription creates a new Subscription object
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(
            username=self.complete_user['username'],
            password=self.complete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.get('/lessons/subscriptions/',
                                   {'subscribe': 'true',
                                    'lesson_id': self.free_lesson.lesson_id},
                                    follow=True)
        self.assertTrue(response, 200)
        self.assertTrue(Subscription.objects.filter(
            lesson=self.free_lesson, user=profile).exists())

    def test_invalid_lesson(self):
        '''
        Invalid lesson passed to subscribe will return user to
        lessons page with error message
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(
            username=self.complete_user['username'],
            password=self.complete_user['password'])
        self.assertTrue(login_successful)

        response = self.client.get('/lessons/subscriptions/',
                                   {'subscribe': 'true',
                                    'lesson_id': self.invalid_lesson_id},
                                   follow=True)

        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response,
                             expected_url=reverse('lessons'),
                             status_code=302,
                             target_status_code=200)
        self.assertFalse(Subscription.objects.filter(
            lesson=self.free_lesson, user=profile).exists())
        self.assertContains(
            response,
            'Invalid request, no lessons have been subscribed')

    def test_invalid_subscribe_request(self):
        '''
        Invalid subscribe argument passed to subscribe will
        return user to lessons page with an error message.
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(
            username=self.complete_user['username'],
            password=self.complete_user['password'])
        self.assertTrue(login_successful)

        response = self.client.get('/lessons/subscriptions/',
                                   {'subscribe': 'INVALID',
                                    'lesson_id': self.free_lesson.lesson_id},
                                   follow=True)

        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response,
                             expected_url=reverse('lessons'),
                             status_code=302,
                             target_status_code=200)
        self.assertFalse(Subscription.objects.filter(
            lesson=self.free_lesson, user=profile).exists())
        self.assertContains(
            response,
            'Invalid request, no lessons have been subscribed')

    def test_subscribe_post_request(self):
        '''
        Post request will return user to
        lessons page an with error message
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(
            username=self.complete_user['username'],
            password=self.complete_user['password'])
        self.assertTrue(login_successful)

        response = self.client.post('/lessons/subscriptions/',
                                    {'subscribe': 'test',
                                     'lesson_id': self.invalid_lesson_id},
                                    follow=True)

        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response,
                             expected_url=reverse('lessons'),
                             status_code=302,
                             target_status_code=200)
        self.assertFalse(Subscription.objects.filter(
            lesson=self.free_lesson, user=profile).exists())
        self.assertContains(
            response,
            'Invalid request, no lessons have been subscribed')

    def test_unsubscribe_valid_request(self):
        '''
        Valid request will remove the subscription
        object for this user / lesson
        '''
        login_successful = self.client.login(
            username=self.incomplete_user['username'],
            password=self.incomplete_user['password'])
        self.assertTrue(login_successful)

        response = self.client.get(
            '/lessons/subscriptions/',
            {'subscribe': 'false',
             'lesson_id': self.subscribed_lesson.lesson_id},
            follow=True)
        self.assertTrue(response, 200)
        self.assertFalse(Subscription.objects.filter(
            lesson=self.subscribed_lesson, user=self.subscribed_user).exists())
