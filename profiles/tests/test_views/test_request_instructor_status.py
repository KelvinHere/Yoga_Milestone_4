from django.test import TestCase
from django.shortcuts import reverse


class TestRequestInstructorStatusView(TestCase):
    fixtures = ['sample_fixtures.json', ]

    def test_logged_out(self):
        '''
        Request to become instructor when logged
        out redirects user to login page
        '''
        response = self.client.get(
            '/profiles/request_instructor_status/request', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            ('/accounts/login/?next=/profiles/request_instructor_status/'
             'request'))

    def test_with_incomplete_profile(self):
        '''
        Request to become instructor without a complete profile
        redirects user back to profile page with error message
        '''
        login_successful = self.client.login(username='incomplete_user',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(
            '/profiles/request_instructor_status/request', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response,
                             expected_url=reverse('profile'),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(
            response,
            'Error, you must complete your profile first.')

    def test_with_complete_profile(self):
        '''
        Valid request to become instructor redirects user to profile
        page without error message and updated button text
        '''
        login_successful = self.client.login(username='complete_user',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(
            '/profiles/request_instructor_status/request',
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response,
                             expected_url=reverse('profile'),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(response, 'Under Review')
        self.assertNotContains(
            response,
            'Error, you must complete your profile first.')
