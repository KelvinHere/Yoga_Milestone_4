from django.test import TestCase


class TestEditProfileView(TestCase):
    fixtures = ['sample_fixtures.json', ]

    def test_logged_out(self):
        '''
        Logged out users will be redirected to login page
        '''
        response = self.client.get('/profiles/edit_profile/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(
            response, '/accounts/login/?next=/profiles/edit_profile/')
        self.assertContains(
            response, 'If you have not created an account yet, then please')

    def test_logged_in(self):
        '''
        Logged in users will be redirected to edit profile page
        '''
        login_successful = self.client.login(username='complete_user',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get('/profiles/edit_profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/edit_profile.html')
        self.assertContains(response, 'Edit your profile')

    def test_edit_profile_post_data(self):
        '''
        Valid POST data updates profie and redirects user to profile page
        '''
        login_successful = self.client.login(username='incomplete_user',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.post(
            '/profiles/edit_profile/',
            {'first_name': 'FirstNameIsHere',
             'last_name': 'LastNameIsHere',
             'profile_description': 'ProfileDescriptionIsHere'},
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            '/profiles/')
        self.assertContains(response, 'FirstNameIsHere')
        self.assertContains(response, 'LastNameIsHere')
        self.assertContains(response, 'ProfileDescriptionIsHere')

    def test_edit_profile_post_form_error(self):
        '''
        Invalid POST data redirects user to profile page with error message
        '''
        login_successful = self.client.login(username='incomplete_user',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.post(
            '/profiles/edit_profile/',
            {'invalid_form_field': 'Invalid'},
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/profiles/')
        self.assertContains(response, 'There was an error in your profile')
