from django.test import TestCase
from django.shortcuts import reverse

from decimal import Decimal

from profiles.models import UserProfile
from lessons.models import Lesson


class TestEditLessonView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.lesson = Lesson.objects.get(lesson_name='B Lesson')

    def test_logged_out(self):
        '''
        Logged out users will be redirect to login page
        '''
        response = self.client.get(
            f'/lessons/edit_lesson/{self.lesson.lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(
            response, ('/accounts/login/?next=/lessons/edit_lesson/'
                       f'{self.lesson.lesson_id}'))
        self.assertContains(response, ('If you have not created an account '
                                       'yet, then please'))

    def test_not_instructor(self):
        '''
        If users is not instructor they are redirected
        home with an error message
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/lessons/edit_lesson/{self.lesson.lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/')
        self.assertContains(response, 'Only instructors can do this.')

    def test_invalid_lesson_id(self):
        '''
        If users is instructor and passes an invalid
        lesson_id they are redirected to instructor
        admin with an error message
        '''
        profile = UserProfile.objects.get(user__username='instructor_1')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/lessons/edit_lesson/INVALID_ID', follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('instructor_admin'),
                             status_code=302,
                             target_status_code=200)
        self.assertTemplateUsed(response, 'lessons/instructor_admin.html')
        self.assertContains(response, ('Invalid lesson ID, no lessons were '
                                       'updated.'))

    def test_valid_lesson_id_wrong_instructor(self):
        '''
        If users is instructor and passes a valid
        lesson_id but they did not create that lesson
        they are returned tp instructor admin with an
        error message
        '''
        another_lesson = Lesson.objects.filter(
            instructor_profile__user__username='instructor_2').first()

        profile = UserProfile.objects.get(user__username='instructor_1')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/lessons/edit_lesson/{another_lesson.lesson_id}', follow=True)
        self.assertRedirects(response,
                             expected_url=reverse('instructor_admin'),
                             status_code=302,
                             target_status_code=200)
        self.assertTemplateUsed(response, 'lessons/instructor_admin.html')
        self.assertContains(response, ('You can only edit your own lessons, '
                                     'please check your username.'))

    def test_valid_lesson_id(self):
        '''
        If users is instructor and passes a valid
        lesson_id they are passed to the edit_lesson
        page with a pre-filled form
        '''
        profile = UserProfile.objects.get(user__username='instructor_1')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/lessons/edit_lesson/{self.lesson.lesson_id}', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/edit_lesson.html')
        self.assertContains(response, self.lesson.lesson_name)
        self.assertContains(response, self.lesson.description)
        self.assertContains(response, self.lesson.card_description)
        self.assertContains(response, self.lesson.video_url)
        self.assertContains(response, self.lesson.time)
        self.assertContains(response, self.lesson.price)

    def test_valid_post_data(self):
        '''
        Valid post data updated the lesson
        '''
        profile = UserProfile.objects.get(user__username='instructor_1')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.post(
            f'/lessons/edit_lesson/{self.lesson.lesson_id}',
            {'lesson_name': 'Updated Lesson Name',
             'card_description': 'Updated Card',
             'description': 'Updated Description',
             'video_url': 'https://www.updated',
             'time': '99',
             'price': '99.99'},
            follow=True)

        self.assertTrue(response, 200)
        self.assertRedirects(response, '/lessons/instructor_admin/')

        updated_lesson = Lesson.objects.get(lesson_name='Updated Lesson Name')
        self.assertEqual(updated_lesson.lesson_name, 'Updated Lesson Name')
        self.assertEqual(updated_lesson.card_description, 'Updated Card')
        self.assertEqual(updated_lesson.description, 'Updated Description')
        self.assertEqual(updated_lesson.video_url, 'https://www.updated')
        self.assertEqual(updated_lesson.time, 99)
        self.assertAlmostEqual(updated_lesson.price, Decimal(99.99))

    def test_invalid_post_data(self):
        '''
        Valid post data updated the lesson
        '''
        profile = UserProfile.objects.get(user__username='instructor_1')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.post(
            f'/lessons/edit_lesson/{self.lesson.lesson_id}',
            {'description': 'Updated from a form with bad price data',
             'price': 'INVALID_PRICE_FOR_FORM'},
            follow=True)

        self.assertTrue(response, 200)
        self.assertRedirects(response, '/lessons/instructor_admin/')

        updated_lesson = Lesson.objects.get(lesson_name='B Lesson')
        self.assertNotEqual(updated_lesson.description,
                            'Updated from a form with bad price data')
        self.assertNotEqual(updated_lesson.price, 'INVALID_PRICE_FOR_FORM')
        self.assertContains(response, ('Invalid form data, please try again. '
                                     'No lessons were updated.'))

