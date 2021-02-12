from django.test import TestCase
from django.shortcuts import reverse
from datetime import datetime

import html
import json

from profiles.models import UserProfile
from lessons.models import Subscription, Lesson, LessonReview


class TestReviewLessonView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.free_lesson = Lesson.objects.filter(is_free=True).first()
        self.invalid_lesson_id = "SDFGGRFVAD"
        self.complete_user = {'username': 'complete_user',
                              'password': 'orange99'}

    def test_review_lesson_logged_out(self):
        ''' Logged out users will be redirect to login page '''
        response = self.client.get(f'/lessons/review_lesson/{self.free_lesson.lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next=/lessons/review_lesson/{self.free_lesson.lesson_id}')
        self.assertContains(response, html.escape('If you have not created an account yet, then please'))

    def test_review_lesson_edit_existing_review_get(self):
        '''
        GET request, existing review redirects user
        to a pre-filled review form
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=self.complete_user['username'],
                                             password=self.complete_user['password'])
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/review_lesson/{self.free_lesson.lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/review.html')
        self.assertContains(response, 'Review for "A lesson"')
        self.assertContains(response, 'Review by complete_user')
        self.assertContains(response, 'Great I loved it!')
        self.assertTrue(LessonReview.objects.filter(lesson=self.free_lesson, profile=profile).exists())

    def test_review_lesson_no_existing_review_get(self):
        '''
        GET request, no existing review redirects
        user to a blank review form
        '''
        lesson = Lesson.objects.get(lesson_name='Z Lesson')
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/review_lesson/{lesson.lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/review.html')
        self.assertContains(response, 'Review for "Z Lesson"')
        self.assertContains(response, 'Review by complete_user')
        self.assertFalse(LessonReview.objects.filter(lesson=lesson, profile=profile).exists())

    def test_review_lesson_invalid_lesson_id(self):
        '''
        Invalid lesson id sends user to home page
        with an error message
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/review_lesson/{self.invalid_lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, 'Cannot create/edit a review for an invalid lesson')

    def test_review_lesson_cant_review_your_own_lesson(self):
        '''
        Instructors trying to review their own lessons are
        redirected back to studo page with error message.
        '''
        lesson = Lesson.objects.get(lesson_name='A lesson')
        login_successful = self.client.login(username='instructor_1',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/review_lesson/{lesson.lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, f'/studio/{lesson.lesson_id}/')
        self.assertTemplateUsed(response, 'studio/studio.html')
        self.assertContains(response, 'You cannot review your own lessons.')

    def test_review_lesson_update_review_post(self):
        '''
        Update an existing review
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        lesson = Lesson.objects.get(lesson_name='Y Lesson')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.post(f'/lessons/review_lesson/{lesson.lesson_id}', {"id": 1,
                                                                "profile": profile.id,
                                                                "lesson": lesson.id,
                                                                "review": "I have been updated",
                                                                "rating_dropdown": 5,
                                                                "date": datetime.now()},
                                                                follow=True)

        self.assertRedirects(response, f'/studio/{lesson.lesson_id}/')
        self.assertContains(response, 'I have been updated')
        self.assertTrue(LessonReview.objects.filter(lesson=lesson, profile=profile).exists())

    def test_review_lesson_create_review_post(self):
        '''
        Post a review where there previously was none
        '''
        profile = UserProfile.objects.get(user__username='incomplete_user')
        lesson = Lesson.objects.get(lesson_name='H Lesson')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.post(f'/lessons/review_lesson/{lesson.lesson_id}', {"id": 1,
                                                                "profile": profile.id,
                                                                "lesson": lesson.id,
                                                                "review": "I am a new review that has just been created",
                                                                "rating_dropdown": 5,
                                                                "date": datetime.now()},
                                                                follow=True)

        self.assertRedirects(response, f'/studio/{lesson.lesson_id}/')
        self.assertContains(response, 'I am a new review that has just been created')
        self.assertTrue(LessonReview.objects.filter(lesson=lesson, profile=profile).exists())

    def test_review_lesson_cant_create_review_on_lesson_not_owned_post(self):
        '''
        User cannot post review on lesson they do not own
        '''
        lesson = Lesson.objects.get(lesson_name='Z Lesson')
        profile = UserProfile.objects.get(user__username='incomplete_user')
        login_successful = self.client.login(username=profile.user.username,
                                            password='orange99')
        self.assertTrue(login_successful)
        self.assertFalse(LessonReview.objects.filter(lesson=lesson, profile=profile).exists())
        response = self.client.post(f'/lessons/review_lesson/{lesson.lesson_id}', {"id": 1,
                                                                "profile": lesson.id,
                                                                "lesson": profile.id,
                                                                "review": "I tried to post on a paid lesson I do not own",
                                                                "rating_dropdown": 5,
                                                                "date": datetime.now()},
                                                                follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('home'),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(response, 'You cannot review a lesson you do not own.')
        self.assertFalse(LessonReview.objects.filter(lesson=lesson, profile=profile).exists())

    def test_review_lesson_stop_user_spoofing_profile_in_form(self):
        '''
        User cannot create / update / a review created
        by another users profile
        '''
        profile = UserProfile.objects.get(user__username='incomplete_user')
        another_profile = UserProfile.objects.get(user__username='complete_user')
        lesson = Lesson.objects.get(lesson_name='H Lesson')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.post(f'/lessons/review_lesson/{lesson.lesson_id}', {"id": 1,
                                                                "profile": another_profile.id,
                                                                "lesson": lesson.id,
                                                                "review": "I am a new review that has just been created",
                                                                "rating_dropdown": 5,
                                                                "date": datetime.now()},
                                                                follow=True)

        self.assertRedirects(response, f'/studio/{lesson.lesson_id}/')
        self.assertContains(response, 'You can only create and edit your own reviews.')

    def test_review_lesson_rating_too_high(self):
        '''
        Test rating too high
        Review rating has to be from 1 to 10
        '''
        invalid_lesson_rating = 11
        profile = UserProfile.objects.get(user__username='incomplete_user')
        lesson = Lesson.objects.get(lesson_name='H Lesson')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.post(f'/lessons/review_lesson/{lesson.lesson_id}', {"id": 1,
                                                                "profile": profile.id,
                                                                "lesson": lesson.id,
                                                                "review": "I am a new review that has just been created",
                                                                "rating_dropdown": invalid_lesson_rating,
                                                                "date": datetime.now()},
                                                                follow=True)

        self.assertRedirects(response, f'/studio/{lesson.lesson_id}/')
        self.assertContains(response, 'You entered an invalid rating, please try again.')
        self.assertFalse(LessonReview.objects.filter(lesson=lesson, profile=profile).exists())

    def test_review_lesson_rating_too_low(self):
        '''
        Test rating too low
        Review rating has to be from 1 to 10
        '''
        invalid_lesson_rating = -1
        profile = UserProfile.objects.get(user__username='incomplete_user')
        lesson = Lesson.objects.get(lesson_name='H Lesson')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.post(f'/lessons/review_lesson/{lesson.lesson_id}', {"id": 1,
                                                                "profile": profile.id,
                                                                "lesson": lesson.id,
                                                                "review": "I am a new review that has just been created",
                                                                "rating_dropdown": invalid_lesson_rating,
                                                                "date": datetime.now()},
                                                                follow=True)

        self.assertRedirects(response, f'/studio/{lesson.lesson_id}/')
        self.assertContains(response, 'You entered an invalid rating, please try again.')
        self.assertFalse(LessonReview.objects.filter(lesson=lesson, profile=profile).exists())
