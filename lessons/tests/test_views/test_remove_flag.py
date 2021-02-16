from django.test import TestCase
from django.shortcuts import reverse

from profiles.models import UserProfile
from lessons.models import LessonReview, LessonReviewFlagged


class TestRemoveFlagView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        # Get a review
        self.review = LessonReview.objects.filter().first()
        # Login as normal user and create flag on that review
        self.flagger_profile = UserProfile.objects.get(
            user__username='incomplete_user')

        login_successful = self.client.login(
            username=self.flagger_profile.user.username,
            password='orange99')
        self.assertTrue(login_successful)
        # Create Flag
        self.review_flag = LessonReviewFlagged.objects.create(
            profile=self.flagger_profile,
            review=self.review)
        # Logout
        self.client.logout()

    def test_logged_out(self):
        ''' Logged out users will be redirect to login page '''
        response = self.client.get(
            '/lessons/remove_flag/',
            follow=True)

        self.assertTrue(response.status_code, 200)
        self.assertRedirects(
            response,
            '/accounts/login/?next=/lessons/remove_flag/')
        self.assertContains(
            response,
            'If you have not created an account yet, then please')
        # Flag exists
        self.assertTrue(
            LessonReviewFlagged.objects.filter(profile=self.flagger_profile,
                                               review=self.review).exists())

    def test_logged_in_not_superuser(self):
        ''' Only superusers can perform this action '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.post(
            '/lessons/remove_flag/',
            data={'flagged_review_pk': self.review_flag.id},
            follow=True)

        self.assertRedirects(response,
                             expected_url=reverse('home'),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(
            response,
            'Only administrators can perform this action.')
        # Flag exists
        self.assertTrue(
            LessonReviewFlagged.objects.filter(profile=self.flagger_profile,
                                               review=self.review).exists())

    def test_get_request(self):
        ''' Remove flag does not accept get requests '''
        profile = UserProfile.objects.get(user__username='kelvinhere')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get('/lessons/remove_flag/',
                                   follow=True)

        self.assertRedirects(response,
                             expected_url=reverse('home'),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(response,
                            'Remove flag does not accept GET requests')
        # Flag exists
        self.assertTrue(
            LessonReviewFlagged.objects.filter(profile=self.flagger_profile,
                                               review=self.review).exists())

    def test_logged_in_as_superuser(self):
        ''' Superusers can perform the remove flag action '''
        profile = UserProfile.objects.get(user__username='kelvinhere')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.post(
            '/lessons/remove_flag/',
            data={'flagged_review_pk': self.review_flag.id},
            follow=True)

        self.assertTrue(response.status_code, 200)
        self.assertContains(response, '"removed_flag": "True"')
        # Flag removed
        self.assertFalse(
            LessonReviewFlagged.objects.filter(
                profile=self.flagger_profile,
                review=self.review).exists())
