import html
from django.test import TestCase
from django.shortcuts import reverse


class ProfileViews(TestCase):
    fixtures = ['sample_fixtures.json', ]

    # Profile Page
    def test_profile_page_logged_out(self):
        '''
        Logged out users will be redirected to login page
        '''
        response = self.client.get('/profiles/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/accounts/login/?next=/profiles/')
        self.assertContains(response, 'If you have not created an account yet, then please')

    def test_profile_page_logged_in(self):
        '''
        Logged in users will be redirected to profile page
        '''
        login_successful = self.client.login(username='complete_user',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, 200)

    # Edit profile
    def test_edit_profile_logged_out(self):
        '''
        Logged out users will be redirected to login page
        '''
        response = self.client.get('/profiles/edit_profile/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/accounts/login/?next=/profiles/edit_profile/')
        self.assertContains(response, 'If you have not created an account yet, then please')

    def test_edit_profile_page_logged_in(self):
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

    def test_update_profile(self):
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

    def test_update_profile_form_error(self):
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

    # Request instructor status view
    def test_request_instructor_status_logged_out(self):
        '''
        Request to become instructor when logged
        out redirects user to login page
        '''
        response = self.client.get(
            '/profiles/request_instructor_status/request', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            '/accounts/login/?next=/profiles/request_instructor_status/request')

    def test_request_instructor_status_with_incomplete_profile(self):
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

    def test_request_instructor_status_with_complete_profile(self):
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

    # Instructor Page
    def test_instructors_no_attributes(self):
        '''
        Renders a list of instructors
        '''
        response = self.client.get('/profiles/instructors/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'Find an instructor to suit you!')

    def test_instructors_invalid_post_request(self):
        '''
        Invalid POST redirects user back to instructors without POST
        '''
        response = self.client.post('/profiles/instructors/', {'some': 'data'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'Find an instructor to suit you!')

    # Instructor view sorting
    def test_instructors_sort_by_name_ascending(self):
        response = self.client.get('/profiles/instructors/', {"sort_by": "user__username", "sort_direction": "asc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('instructor_1') < html_str.index('instructor_2'))
        self.assertTrue(html_str.index('instructor_2') < html_str.index('instructor_3'))

    def test_instructors_sort_by_name_descending(self):
        response = self.client.get('/profiles/instructors/', {"sort_by": "user__username", "sort_direction": "desc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('instructor_1') > html_str.index('instructor_2'))
        self.assertTrue(html_str.index('instructor_2') > html_str.index('instructor_3'))

    def test_instructors_sort_by_rating_ascending(self):
        response = self.client.get('/profiles/instructors/', {"sort_by": "rating", "sort_direction": "asc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('6 / 10') < html_str.index('10 / 10'))

    def test_instructors_sort_by_rating_descending(self):
        response = self.client.get('/profiles/instructors/', {"sort_by": "rating", "sort_direction": "desc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('6 / 10') > html_str.index('10 / 10'))

    def test_instructors_sort_by_lesson_number_ascending(self):
        response = self.client.get('/profiles/instructors/', {"sort_by": "lesson_count", "sort_direction": "asc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('instructor_3') < html_str.index('instructor_2'))

    def test_instructors_sort_by_lesson_number_descending(self):
        response = self.client.get('/profiles/instructors/', {"sort_by": "lesson_count", "sort_direction": "desc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('instructor_3') > html_str.index('instructor_2'))

    # Instructor view Query
    def test_instructor_query(self):
        response = self.client.get('/profiles/instructors/', {"q": "instructor_1"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertNotContains(response, 'instructor_2')
        self.assertNotContains(response, 'instructor_3')

    # Instructor view, Stacked Query & Sorting
    def test_instructor_query_and_sort_name_ascending(self):
        response = self.client.get('/profiles/instructors/', {"q": "instructor", "sort_by": "user__username", "sort_direction": "asc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertContains(response, 'instructor_2')
        self.assertContains(response, 'instructor_3')
        html_str = response.content.decode("utf-8")
        self.assertLess(html_str.index('instructor_1'), html_str.index('instructor_2'))
        self.assertLess(html_str.index('instructor_2'), html_str.index('instructor_3'))

    def test_instructor_query_and_sort_name_descending(self):
        response = self.client.get('/profiles/instructors/', {"q": "instructor", "sort_by": "user__username", "sort_direction": "desc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertContains(response, 'instructor_2')
        self.assertContains(response, 'instructor_3')
        html_str = response.content.decode("utf-8")
        self.assertGreater(html_str.index('instructor_1'), html_str.index('instructor_2'))
        self.assertGreater(html_str.index('instructor_2'), html_str.index('instructor_3'))

    def test_instructor_query_and_sort_rating_ascending(self):
        response = self.client.get('/profiles/instructors/', {"q": "instructor", "sort_by": "rating", "sort_direction": "asc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertContains(response, 'instructor_2')
        self.assertContains(response, 'instructor_3')
        html_str = response.content.decode("utf-8")
        self.assertLess(html_str.index('6 / 10'), html_str.index('10 / 10'))

    def test_instructor_query_and_sort_rating_descending(self):
        response = self.client.get('/profiles/instructors/', {"q": "instructor", "sort_by": "rating", "sort_direction": "desc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertContains(response, 'instructor_2')
        self.assertContains(response, 'instructor_3')
        html_str = response.content.decode("utf-8")
        self.assertGreater(html_str.index('6 / 10'), html_str.index('10 / 10'))

    def test_instructor_query_and_sort_lesson_count_ascending(self):
        response = self.client.get('/profiles/instructors/', {"q": "instructor", "sort_by": "lesson_count", "sort_direction": "asc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertContains(response, 'instructor_2')
        self.assertContains(response, 'instructor_3')
        html_str = response.content.decode("utf-8")
        self.assertLess(html_str.index('instructor_3'), html_str.index('instructor_1'))

    def test_instructor_query_and_sort_lesson_count_descending(self):
        response = self.client.get('/profiles/instructors/', {"q": "instructor", "sort_by": "lesson_count", "sort_direction": "desc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertContains(response, 'instructor_2')
        self.assertContains(response, 'instructor_3')
        html_str = response.content.decode("utf-8")
        self.assertGreater(html_str.index('instructor_3'), html_str.index('instructor_1'))
