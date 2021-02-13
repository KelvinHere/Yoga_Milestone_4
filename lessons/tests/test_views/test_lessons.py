from django.test import TestCase

import html

from profiles.models import UserProfile
from lessons.models import Subscription, Lesson


class TestLessonsView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.instructor = UserProfile.objects.filter(is_instructor=True).first()

        profile = UserProfile.objects.get(user__username='kelvinhere')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

    def test_get_lessons(self):
        '''
        Renders a list of all lessons
        '''
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        self.assertContains(response, 'All Lessons')

    def test_lessons_with_valid_instructor_filter(self):
        '''
        Displays the instructors profile and all their
        lessons underneath
        '''
        response = self.client.get('/lessons/', {'instructor': self.instructor.id}, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        self.assertContains(response, self.instructor.user.username)
        self.assertContains(response, html.escape(self.instructor.profile_description))
       
    def test_lesson_query(self):
        '''
        Only show queried lessons
        '''
        response = self.client.get('/lessons/?q=z')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        
        self.assertContains(response, 'All Lessons')
        self.assertContains(response, 'Z Lesson')
        
        self.assertNotContains(response, 'A Lesson')
        self.assertNotContains(response, 'B Lesson')
        self.assertNotContains(response, 'H Lesson')
        self.assertNotContains(response, 'Y Lesson')

    def test_sort_name_ascending(self):
        response = self.client.get('/lessons/', {"sort": "lesson_name", "direction": "asc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('A Lesson') < html_str.index('B Lesson'))
        self.assertTrue(html_str.index('Y Lesson') < html_str.index('Z Lesson'))

    def test_sort_name_descending(self):
        response = self.client.get('/lessons/', {"sort": "lesson_name", "direction": "desc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('A Lesson') > html_str.index('B Lesson'))
        self.assertTrue(html_str.index('Y Lesson') > html_str.index('Z Lesson'))

    def test_sort_rating_ascending(self):
        response = self.client.get('/lessons/', {"sort": "rating", "direction": "asc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('6/10') < html_str.index('10/10'))

    def test_sort_rating_descending(self):
        response = self.client.get('/lessons/', {"sort": "rating", "direction": "desc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('6/10') > html_str.index('10/10'))

    def test_sort_price_ascending(self):
        response = self.client.get('/lessons/', {"sort": "price", "direction": "asc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('€35.99') > html_str.index('€24.99'))

    def test_sort_price_descending(self):
        response = self.client.get('/lessons/', {"sort": "price", "direction": "desc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')
        html_str = response.content.decode("utf-8")
        self.assertTrue(html_str.index('€35.99') < html_str.index('€24.99'))
