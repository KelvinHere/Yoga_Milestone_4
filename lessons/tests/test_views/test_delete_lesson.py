from django.test import TestCase

import html

from profiles.models import UserProfile
from lessons.models import Subscription, Lesson


class TestDeleteLessonView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.instructor = UserProfile.objects.filter(is_instructor=True).first()
        self.free_lesson = Lesson.objects.filter(is_free=True).first()
        self.paid_lesson = Lesson.objects.filter(is_free=False, lesson_name='Z Lesson').first()
        self.invalid_lesson_id = "SDFGGRFVAD"
        self.subscribed_user = UserProfile.objects.get(id=5)  # = incomplete_user
        self.subscribed_lesson = Lesson.objects.get(id=2)
        self.subscription = Subscription.objects.get(lesson=self.subscribed_lesson,
                                                     user=self.subscribed_user)
        self.complete_user = {'username': 'complete_user',
                              'password': 'orange99'}
        self.incomplete_user = {'username': 'incomplete_user',
                                'password': 'orange99'}
        self.instructor_credentials = {'username': 'instructor_2',
                                       'password': 'orange99'}

    def test_logged_out(self):
        '''
        Logged out out users redirected to sign in
        '''
        lesson_to_delete = Lesson.objects.get(lesson_name='Y Lesson')
        response = self.client.get(f'/lessons/delete_lesson/{lesson_to_delete.lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next=/lessons/delete_lesson/{lesson_to_delete.lesson_id}')
        self.assertContains(response, html.escape('If you have not created an account yet, then please'))

    def test_delete_lesson_valid_request(self):
        '''
        Delete lesson
        '''
        lesson_to_delete = Lesson.objects.get(lesson_name='Y Lesson')
        instructor = lesson_to_delete.instructor_profile
        login_successful = self.client.login(username=instructor.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/delete_lesson/{lesson_to_delete.lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/lessons/instructor_admin/')
        self.assertFalse(Lesson.objects.filter(lesson_name='Y Lesson').exists())
        self.assertContains(response, 'Lesson deleted')

    def test_invalid_lessonid(self):
        '''
        Deleting and invalid lesson will redirect user
        back to instructor admin with error message.
        '''
        login_successful = self.client.login(username='instructor_1',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/delete_lesson/{self.invalid_lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/lessons/instructor_admin/')
        self.assertContains(response, 'Invalid lesson ID, no lessons were deleted.')

    def test_delete_lesson_not_your_lesson(self):
        '''
         Trying to delete someone elses lesson redirects you to
         instructor_admin with an error message
        '''
        not_your_lesson = Lesson.objects.get(lesson_name='A lesson')
        login_successful = self.client.login(username='instructor_3',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/delete_lesson/{not_your_lesson.lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/lessons/instructor_admin/')
        self.assertTrue(Lesson.objects.filter(lesson_name='A lesson').exists())
        self.assertContains(response, 'This lesson does not belong to you')

    def test_delete_lesson_paid_lesson_customers_have_bought(self):
        '''
        Cannot delete a lesson that has been bought by customers
        '''
        lesson_sold = Lesson.objects.get(lesson_name='Z Lesson')
        login_successful = self.client.login(username='instructor_2',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/delete_lesson/{lesson_sold.lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/lessons/instructor_admin/')
        self.assertTrue(Lesson.objects.filter(lesson_name='Z Lesson').exists())
        self.assertContains(response, 'You cannot delete a lesson customers have')

    def test_delete_lesson_paid_lesson_customers_have_not_bought(self):
        '''
        Paid lessons with no sales can be deleted
        '''
        lesson_not_sold = Lesson.objects.get(lesson_name='B lesson')
        login_successful = self.client.login(username='instructor_1',
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.get(f'/lessons/delete_lesson/{lesson_not_sold.lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/lessons/instructor_admin/')
        self.assertFalse(Lesson.objects.filter(lesson_name='B lesson').exists())
        self.assertContains(response, 'Lesson deleted')