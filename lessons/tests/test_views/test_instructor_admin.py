from django.test import TestCase

import html

from profiles.models import UserProfile


class TestInstructorAdminView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.user = {'username': 'complete_user',
                     'password': 'orange99'}
        self.instructor = {'username': 'instructor_2',
                                       'password': 'orange99'}

    def test_logged_out(self):
        '''
        Logged out users will be redirect to login page
        '''
        response = self.client.get('/lessons/instructor_admin/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(
            response, '/accounts/login/?next=/lessons/instructor_admin/')
        self.assertContains(
            response, 'If you have not created an account yet, then please')

    def test_not_instructor(self):
        '''
        A non instructor will be redirected home with an error message
        '''
        login_successful = self.client.login(username=self.user['username'],
                                             password=self.user['password'])
        self.assertTrue(login_successful)

        response = self.client.get('/lessons/instructor_admin/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, 'Only instructors can do this.')

    def test_is_an_instructor(self):
        '''
        Instructors can view this page and see lessons / sales
        '''
        login_successful = self.client.login(
            username=self.instructor['username'],
            password=self.instructor['password'])
        self.assertTrue(login_successful)

        response = self.client.get('/lessons/instructor_admin/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/instructor_admin.html')
        self.assertContains(response, 'Lesson Admin for instructor_2')
        # Contains instructors lessons
        self.assertContains(response,
                            html.escape("Instructor 2's first lesson"))
        # Contains instructors sales
        self.assertContains(response, html.escape("24.99 - 30%"))

    def test_instructor_not_completed_profile_description(self):
        '''
        New instructors who have not completed their
        instructor profile will be shown a danger
        button prompting them to complete it.
        '''
        login_successful = self.client.login(
            username=self.instructor['username'],
            password=self.instructor['password'])
        self.assertTrue(login_successful)

        # Remove profile description from instructor
        UserProfile.objects.filter(
            user__username=self.instructor['username']).update(
                profile_description='')

        response = self.client.get('/lessons/instructor_admin/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/instructor_admin.html')

        # Contains Update Instructor Profile button
        self.assertContains(response,
                            ('you are now an instructor, please complete your '
                             'instructor profile and have a quick read of '
                             'support before you create any lessons, as your '
                             'card and profile data help users choose your '
                             'lessons.  Thankyou.'))

        self.assertContains(response, 'Complete Instructor Profile')

    def test_instructor_not_completed_card_description(self):
        '''
        New instructors who have not completed their
        instructor card will be shown a danger
        button prompting them to complete it.
        '''
        login_successful = self.client.login(
            username=self.instructor['username'],
            password=self.instructor['password'])
        self.assertTrue(login_successful)

        # Remove profile description from instructor
        UserProfile.objects.filter(
            user__username=self.instructor['username']).update(
                card_description='')

        response = self.client.get('/lessons/instructor_admin/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/instructor_admin.html')

        # Contains Update Instructor Profile button
        self.assertContains(response,
                            ('you are now an instructor, please complete your '
                             'instructor profile and have a quick read of '
                             'support before you create any lessons, as your '
                             'card and profile data help users choose your '
                             'lessons.  Thankyou.'))

        self.assertContains(response, 'Complete Instructor Profile')
