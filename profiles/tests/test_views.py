from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse

from profiles.models import UserProfile


# Create your tests here.
class ProfileViews(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='12345',
            email='user1@test.com',
            is_active=True
            )
        self.user1.save()

    def tearDown(self):
        self.user1.delete()

    def test_profile_page_logged_out(self):
        response = self.client.get('/profiles/')
        self.assertRedirects(response, '/accounts/login/?next=/profiles/')

    def test_profile_page_logged_in(self):
        login_successful = self.client.login(username='user1',
                                             password='12345')
        self.assertTrue(login_successful)

        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, 200)

    def test_request_instructor_status_with_incomplete_profile(self):
        login_successful = self.client.login(username='user1',
                                             password='12345')
        self.assertTrue(login_successful)

        response = self.client.get('/profiles/request_instructor_status/request', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, expected_url=reverse('profile'), status_code=302, target_status_code=200)
        self.assertContains(response, 'Error, you must complete your profile first.')

    def test_request_instructor_status_with_complete_profile(self):
        login_successful = self.client.login(username='user1',
                                             password='12345')
        self.assertTrue(login_successful)

        # Complete profile for user1
        profile = UserProfile.objects.get(user=self.user1)
        profile.first_name = 'Ben'
        profile.last_name = 'Smith'
        profile.profile_description = 'My description here'
        profile.image = 'www.myimage.jpg'
        profile.save()

        response = self.client.get('/profiles/request_instructor_status/request', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, expected_url=reverse('profile'), status_code=302, target_status_code=200)
        self.assertNotContains(response, 'Error, you must complete your profile first.')