from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse

from profiles.models import UserProfile
from lessons.models import Lesson


# Create your tests here.
class ProfileViews(TestCase):
    fixtures = ['sample_fixtures.json', ]

    # Profile Page
    def test_profile_page_logged_out(self):
        response = self.client.get('/profiles/')
        self.assertRedirects(response, '/accounts/login/?next=/profiles/')

    def test_profile_page_logged_in(self):
        login_successful = self.client.login(username='complete_user',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, 200)

    # Edit profile
    def test_edit_profile_logged_out(self):
        response = self.client.get('/profiles/edit_profile/')
        self.assertRedirects(response, '/accounts/login/?next=/profiles/edit_profile/')

    def test_edit_profile_page_logged_in(self):
        login_successful = self.client.login(username='complete_user',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get('/profiles/edit_profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/edit_profile.html')
        self.assertContains(response, 'Edit your profile')

    def test_update_profile(self):
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

    def test_update_profile_form_error(self):
        login_successful = self.client.login(username='incomplete_user',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.post(
            '/profiles/edit_profile/',
            {'first_name': False,
             'last_name': False,
             'profile_description': 0.11},
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/profiles/')
        self.assertContains(response, 'There was an error')

    # Request instructor status view
    def test_request_instructor_status_logged_out(self):
        response = self.client.get(
            '/profiles/request_instructor_status/request', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            '/accounts/login/?next=/profiles/request_instructor_status/request')

    def test_request_instructor_status_with_incomplete_profile(self):
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

    def test_request_instructor_status_with_complete_profile(self):
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
        self.assertNotContains(
            response,
            'Error, you must complete your profile first.')
