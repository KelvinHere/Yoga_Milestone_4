from django.test import TestCase
from django.shortcuts import reverse

from profiles.models import UserProfile
from lessons.models import LessonReviewFlagged, LessonReview


class TestSuperUserAdminViews(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        # Set up review flags
        flagger_profile = UserProfile.objects.get(id=5)
        self.review_1 = LessonReview.objects.get(id=1)
        self.review_2 = LessonReview.objects.get(id=2)
        LessonReviewFlagged.objects.create(profile=flagger_profile,
                                           review=self.review_1)
        LessonReviewFlagged.objects.create(profile=flagger_profile,
                                           review=self.review_2)

    def test_logged_out(self):
        '''
        Logged out users will be redirected to login page
        '''
        self.client.logout()
        response = self.client.get('/superuser_admin/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(
            response, '/accounts/login/?next=/superuser_admin/')
        self.assertContains(response, ('If you have not created an account '
                                       'yet, then please'))

    def test_logged_in_not_superuser(self):
        '''
        Non superusers cannot access this page
        '''
        login_successful = self.client.login(username='complete_user',
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get('/superuser_admin/', follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('home'),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(response, 'Sorry only administrators can do this')

    def test_as_superuser(self):
        '''
        Superusers can access this page and view
        all requests, instructors and flags.
        '''
        login_successful = self.client.login(username='kelvinhere',
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get('/superuser_admin/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/superuser_admin.html')

        # Instructors
        self.assertContains(response, 'Active instructors')
        self.assertContains(response, 'instructor_1')
        self.assertContains(response, 'instructor_2')
        self.assertContains(response, 'instructor_3')

        # +1 user wants to become an instructor
        self.assertContains(response, 'User requests to become instructors')
        self.assertContains(
            response,
            'Requests <span class="text-white bg-danger rounded px-2 py-1">+1')

        # +2 reviews are flagged
        self.assertContains(response, 'Flagged Reviews')
        self.assertContains(
            response,
            'Flagged <span class="text-white bg-danger rounded px-2 py-1">+2')
        self.assertContains(response, self.review_1.review)
        self.assertContains(response, self.review_2.review)
