from django.test import TestCase


class TestInstructorsView(TestCase):
    fixtures = ['sample_fixtures.json', ]

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
        response = self.client.post(
            '/profiles/instructors/', {'some': 'data'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'Find an instructor to suit you!')

    # Instructor view sorting
    def test_instructors_sort_by_name_ascending(self):
        response = self.client.get(
            '/profiles/instructors/', {"sort_by": "user__username",
                                       "sort_direction": "asc"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(
            html_str.index('instructor_1') < html_str.index('instructor_2'))
        self.assertTrue(
            html_str.index('instructor_2') < html_str.index('instructor_3'))

    def test_instructors_sort_by_name_descending(self):
        response = self.client.get(
            '/profiles/instructors/', {"sort_by": "user__username",
                                       "sort_direction": "desc"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(
            html_str.index('instructor_1') > html_str.index('instructor_2'))
        self.assertTrue(
            html_str.index('instructor_2') > html_str.index('instructor_3'))

    def test_instructors_sort_by_rating_ascending(self):
        response = self.client.get(
            '/profiles/instructors/', {"sort_by": "rating",
                                       "sort_direction": "asc"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('6 / 10') < html_str.index('10 / 10'))

    def test_instructors_sort_by_rating_descending(self):
        response = self.client.get(
            '/profiles/instructors/', {"sort_by": "rating",
                                       "sort_direction": "desc"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('6 / 10') > html_str.index('10 / 10'))

    def test_instructors_sort_by_lesson_number_ascending(self):
        response = self.client.get(
            '/profiles/instructors/', {"sort_by": "lesson_count",
                                       "sort_direction": "asc"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(
            html_str.index('instructor_3') < html_str.index('instructor_2'))

    def test_instructors_sort_by_lesson_number_descending(self):
        response = self.client.get(
            '/profiles/instructors/', {"sort_by": "lesson_count",
                                       "sort_direction": "desc"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(
            html_str.index('instructor_3') > html_str.index('instructor_2'))

    # Instructor view Query
    def test_instructor_query(self):
        response = self.client.get(
            '/profiles/instructors/', {"q": "instructor_1"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertNotContains(response, 'instructor_2')
        self.assertNotContains(response, 'instructor_3')

    def test_instructor_query_zero_results(self):
        ''' No results on a query returns error message '''
        response = self.client.get(
            '/profiles/instructors/', {"q": "NO_ONE_IS_CALLED_THIS"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertNotContains(response, 'instructor_1')
        self.assertNotContains(response, 'instructor_2')
        self.assertNotContains(response, 'instructor_3')
        self.assertContains(response, "Your query returned no instructors")

    # Instructor view, Stacked Query & Sorting
    def test_instructor_query_and_sort_name_ascending(self):
        response = self.client.get(
            '/profiles/instructors/', {"q": "instructor",
                                       "sort_by": "user__username",
                                       "sort_direction": "asc"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertContains(response, 'instructor_2')
        self.assertContains(response, 'instructor_3')
        html_str = response.content.decode("utf-8")
        self.assertLess(
            html_str.index('instructor_1'), html_str.index('instructor_2'))
        self.assertLess(
            html_str.index('instructor_2'), html_str.index('instructor_3'))

    def test_instructor_query_and_sort_name_descending(self):
        response = self.client.get(
            '/profiles/instructors/', {"q": "instructor",
                                       "sort_by": "user__username",
                                       "sort_direction": "desc"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertContains(response, 'instructor_2')
        self.assertContains(response, 'instructor_3')
        html_str = response.content.decode("utf-8")
        self.assertGreater(
            html_str.index('instructor_1'), html_str.index('instructor_2'))
        self.assertGreater(
            html_str.index('instructor_2'), html_str.index('instructor_3'))

    def test_instructor_query_and_sort_rating_ascending(self):
        response = self.client.get(
            '/profiles/instructors/', {"q": "instructor",
                                       "sort_by": "rating",
                                       "sort_direction": "asc"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertContains(response, 'instructor_2')
        self.assertContains(response, 'instructor_3')
        html_str = response.content.decode("utf-8")
        self.assertLess(html_str.index('6 / 10'), html_str.index('10 / 10'))

    def test_instructor_query_and_sort_rating_descending(self):
        response = self.client.get(
            '/profiles/instructors/', {"q": "instructor",
                                       "sort_by": "rating",
                                       "sort_direction": "desc"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertContains(response, 'instructor_2')
        self.assertContains(response, 'instructor_3')
        html_str = response.content.decode("utf-8")
        self.assertGreater(html_str.index('6 / 10'), html_str.index('10 / 10'))

    def test_instructor_query_and_sort_lesson_count_ascending(self):
        response = self.client.get(
            '/profiles/instructors/', {"q": "instructor",
                                       "sort_by": "lesson_count",
                                       "sort_direction": "asc"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertContains(response, 'instructor_2')
        self.assertContains(response, 'instructor_3')
        html_str = response.content.decode("utf-8")
        self.assertLess(
            html_str.index('instructor_3'), html_str.index('instructor_1'))

    def test_instructor_query_and_sort_lesson_count_descending(self):
        response = self.client.get(
            '/profiles/instructors/', {"q": "instructor",
                                       "sort_by": "lesson_count",
                                       "sort_direction": "desc"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')
        self.assertContains(response, 'instructor_1')
        self.assertContains(response, 'instructor_2')
        self.assertContains(response, 'instructor_3')
        html_str = response.content.decode("utf-8")
        self.assertGreater(
            html_str.index('instructor_3'), html_str.index('instructor_1'))

    # Pagination
    def test_pagination_page_does_not_exist(self):
        '''
        A user trying to access a paginated page that
        does not exist will get an error message and
        returned to page 1
        '''
        try_page = 950
        response = self.client.get(f'/profiles/instructors/?page={try_page}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/instructors.html')

        self.assertContains(response, ('Page does not exist, returning '
                                       'to page 1'))
        self.assertContains(response, 'Page 1 of')
