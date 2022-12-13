from django.test import TestCase


class TestProfileView(TestCase):
    fixtures = ['sample_fixtures.json', ]

    def test_profile_page_logged_out(self):
        '''
        Logged out users will be redirected to login page
        '''
        response = self.client.get('/profiles/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/accounts/login/?next=/profiles/')
        self.assertContains(
            response, 'If you have not created an account yet, then please')

    def test_profile_page_logged_in(self):
        '''
        Logged in users will be redirected to profile page
        '''
        login_successful = self.client.login(username='complete_user',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, 200)
