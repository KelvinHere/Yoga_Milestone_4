from django.test import TestCase
from django.shortcuts import reverse

import html

from profiles.models import UserProfile
from lessons.models import LessonReview, LessonReviewFlagged


class TestFlagReviewView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.review = LessonReview.objects.filter().first()

    def test_logged_out(self):
        ''' Logged out users will be redirect to login page '''
        response = self.client.get(
            f'/lessons/flag_review/{self.review.pk}/{self.review.lesson.id}',
            follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/lessons/flag_review/{self.review.pk}/{self.review.lesson.id}')
        self.assertContains(
            response,
            html.escape('If you have not created an account yet, then please'))

    def test_invalid_review(self):
        '''
        Flagging an invalid review will redirect
        user back to studio with an error message
        '''
        invalid_review_pk = 342331
        lesson_id = self.review.lesson.lesson_id
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(
            f'/lessons/flag_review/{invalid_review_pk}/{lesson_id}',
            follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('studio', args=(lesson_id,)),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(response, 'Invalid review, please contact support if you think this is an error')

    def test_flag_review(self):
        '''
        Flagging a review will redirect user
        back to sutdio page with an error message
        '''
        review_pk = self.review.pk
        lesson_id = self.review.lesson.lesson_id

        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/flag_review/{review_pk}/{lesson_id}',
                                   follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('studio', args=(lesson_id,)),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(response, 'review has been flagged and will be reviewed by an administrator soon')
        self.assertTrue(LessonReviewFlagged.objects.filter(
            profile=profile, review=self.review).exists())

    def test_re_flag_review(self):
        '''
        Flagging a review more than once redirects user
        back to studio page with error
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        
        # Create review flag
        LessonReviewFlagged.objects.create(profile=profile,
                                           review=self.review)
        review_pk = self.review.pk
        lesson_id = self.review.lesson.lesson_id
        response = self.client.get(
            f'/lessons/flag_review/{review_pk}/{lesson_id}', follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('studio', args=(lesson_id,)),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(
            response,
            'You have already flagged complete_user&#x27;s review, it will be reviewd by an administrator soon')

    def test_flags_appear_in_superuser_admin(self):
        '''
        Flags will appear on superuser admin page
        '''
        # Login as user and create flag
        profile = UserProfile.objects.get(user__username='incomplete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        LessonReviewFlagged.objects.create(profile=profile,
                                           review=self.review)
        self.client.logout()

        # Login as superuser
        login_successful = self.client.login(username='kelvinhere',
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get('/superuser_admin/')
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/superuser_admin.html')
        self.assertContains(response, 'Flagged Reviews')
        self.assertContains(response, 'Review by : complete_user')
        self.assertContains(response, 'On lesson: A Lesson')
        self.assertContains(response, 'Flagged By: incomplete_user')
