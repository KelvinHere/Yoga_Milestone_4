from django.test import TestCase
from django.shortcuts import reverse

from lessons.models import Subscription
from profiles.models import UserProfile


class TestIndexView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def test_logged_out(self):
        ''' Logged out users will be redirect to login page '''
        self.client.logout()
        response = self.client.get('/update_instructor_status/1/1', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(
            response, '/accounts/login/?next=/update_instructor_status/1/1')
        self.assertContains(response, ('If you have not created an account '
                                       'yet, then please'))

    def test_not_superuser(self):
        '''
        Non superusers cannot access this view
        '''
        login_successful = self.client.login(username='complete_user',
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get('/update_instructor_status/1/1', follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('home'),
                             status_code=302,
                             target_status_code=200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_superuser_update_invalid_user(self):
        '''
        Superusers submitting an invalid user_to_update
        will be redirected back to superuser_admin
        '''
        login_successful = self.client.login(username='kelvinhere',
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            '/update_instructor_status/INVALID_USER/accept',
            follow=True)

        self.assertRedirects(response,
                             expected_url=reverse('superuser_admin'),
                             status_code=302,
                             target_status_code=200)
        self.assertTemplateUsed(response, 'home/superuser_admin.html')
        self.assertContains(response, 'User does not exist.')

    def test_superuser_update_status_not_accept(self):
        '''
        Superusers submitting any status other than accept will
        default to the request being rejected
        '''
        # User who has requested instructor status
        request_from = UserProfile.objects.get(user__username='complete_user')

        # Superuser
        login_successful = self.client.login(username='kelvinhere',
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/update_instructor_status/{request_from}/accept',
            follow=True)

        self.assertRedirects(response,
                             expected_url=reverse('superuser_admin'),
                             status_code=302,
                             target_status_code=200)
        self.assertTemplateUsed(response, 'home/superuser_admin.html')
        self.assertContains(response, f'id="acive-instructor-{request_from.user.username}"')