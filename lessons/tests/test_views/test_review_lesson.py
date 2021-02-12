from django.test import TestCase
from django.shortcuts import reverse

import html
import json

from profiles.models import UserProfile
from lessons.models import Subscription, Lesson, LessonReview


class TestReviewLessonView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        print('#')
        #self.instructor = UserProfile.objects.filter(is_instructor=True).first()
        self.free_lesson = Lesson.objects.filter(is_free=True).first()
        #self.paid_lesson = Lesson.objects.filter(is_free=False, lesson_name='Z Lesson').first()
        self.invalid_lesson_id = "SDFGGRFVAD"
        #self.subscribed_user = UserProfile.objects.get(id=5)  # = incomplete_user
        #self.subscribed_lesson = Lesson.objects.get(id=2)
        #self.subscription = Subscription.objects.get(lesson=self.subscribed_lesson,
        #                                             user=self.subscribed_user)
        self.complete_user = {'username': 'complete_user',
                              'password': 'orange99'}
        #self.incomplete_user = {'username': 'incomplete_user',
        #                        'password': 'orange99'}
        #self.instructor_credentials = {'username': 'instructor_2',
        #                               'password': 'orange99'}

    def test_review_lesson_logged_out(self):
        ''' Logged out users will be redirect to login page '''
        response = self.client.get(f'/lessons/review_lesson/{self.free_lesson.lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next=/lessons/review_lesson/{self.free_lesson.lesson_id}')
        self.assertContains(response, html.escape('If you have not created an account yet, then please'))

    def test_review_lesson_existing_review(self):
        '''
        GET request redirects to a pre-filled review form 
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=self.complete_user['username'],
                                             password=self.complete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/review_lesson/{self.free_lesson.lesson_id}', follow=True)
        self.assertTemplateUsed(response, 'lessons/review.html')
        self.assertContains(response, 'Review for "A lesson"')
        self.assertContains(response, 'Review by complete_user')
        self.assertContains(response, 'Great I loved it!')
        self.assertTrue(LessonReview.objects.filter(lesson=self.free_lesson, profile=profile).exists())

    def test_review_lesson_no_existing_review(self):
        '''
        GET request redirects to a blank review form 
        '''
        lesson = Lesson.objects.get(lesson_name='Z Lesson')
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/review_lesson/{lesson.lesson_id}', follow=True)
        self.assertTemplateUsed(response, 'lessons/review.html')
        self.assertContains(response, 'Review for "Z Lesson"')
        self.assertContains(response, 'Review by complete_user')
        self.assertFalse(LessonReview.objects.filter(lesson=lesson, profile=profile).exists())

    def test_review_lesson_invalid_lesson_id(self):
        '''
        Invalid lesson id sends user to home page
        with error message
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/review_lesson/{self.invalid_lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, 'Cannot create/edit a review for an invalid lesson')

'''
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
'''