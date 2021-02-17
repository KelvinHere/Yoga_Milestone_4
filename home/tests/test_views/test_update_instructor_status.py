from django.test import TestCase
from django.shortcuts import reverse

from profiles.models import UserProfile


class TestIndexView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def test_logged_out(self):
        ''' Logged out users will be redirect to login page '''
        self.client.logout()
        response = self.client.get('/update_instructor_status/1/1',
                                   follow=True)
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

        response = self.client.get('/update_instructor_status/1/1',
                                   follow=True)
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

    def test_superuser_update_status_invalid(self):
        '''
        Superusers submitting an invalid stats
        will get an error messagge
        '''
        # User who has requested instructor status and check status
        request_from = UserProfile.objects.get(user__username='complete_user')
        # Is not instructor
        self.assertEqual(request_from.is_instructor, False)
        # Requested to become instructor
        self.assertEqual(request_from.requested_instructor_status, True)

        # Superuser
        login_successful = self.client.login(username='kelvinhere',
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/update_instructor_status/{request_from}/INVALIDSTATUS',
            follow=True)

        self.assertRedirects(response,
                             expected_url=reverse('superuser_admin'),
                             status_code=302,
                             target_status_code=200)
        self.assertTemplateUsed(response, 'home/superuser_admin.html')

        # Refresh request_from
        request_from = UserProfile.objects.get(user__username='complete_user')
        # Requested still here
        self.assertEqual(request_from.requested_instructor_status, True)
        # is_instructor still
        self.assertEqual(request_from.is_instructor, False)

        self.assertContains(response, ('Submitted invalid status. No '
                                       'changes made.'))

    def test_superuser_update_status_reject(self):
        '''
        Superusers submitting rejcet status will
        reject the users request
        '''
        # User who has requested instructor status and check status
        request_from = UserProfile.objects.get(user__username='complete_user')
        # Is not instructor
        self.assertEqual(request_from.is_instructor, False)
        # Requested to become instructor
        self.assertEqual(request_from.requested_instructor_status, True)

        # Superuser
        login_successful = self.client.login(username='kelvinhere',
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/update_instructor_status/{request_from}/reject',
            follow=True)

        self.assertRedirects(response,
                             expected_url=reverse('superuser_admin'),
                             status_code=302,
                             target_status_code=200)
        self.assertTemplateUsed(response, 'home/superuser_admin.html')
        self.assertNotContains(
            response, f'id="acive-instructor-{request_from.user.username}"')

        # Refresh request_from
        request_from = UserProfile.objects.get(user__username='complete_user')
        # Request removed
        self.assertNotEqual(request_from.requested_instructor_status, True)
        # is_instructor still false
        self.assertEqual(request_from.is_instructor, False)

    def test_superuser_update_status_accept(self):
        '''
        Superusers submitting valid user and accept status
        will update the users is_instructor status to True
        and user will be added to Active instructors
        list on superuser_admin page.
        '''
        # User who has requested instructor status and check status
        request_from = UserProfile.objects.get(user__username='complete_user')
        # Is not instructor
        self.assertEqual(request_from.is_instructor, False)
        # Requested to become instructor
        self.assertEqual(request_from.requested_instructor_status, True)

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
        self.assertContains(
            response, f'id="acive-instructor-{request_from.user.username}"')

        # Refresh request_from and check is_instructor has been updated
        request_from = UserProfile.objects.get(user__username='complete_user')
        self.assertEqual(request_from.is_instructor, True)
