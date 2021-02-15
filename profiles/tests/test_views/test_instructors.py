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
