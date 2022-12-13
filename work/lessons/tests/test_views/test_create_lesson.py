from django.test import TestCase
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from decimal import Decimal

from profiles.models import UserProfile
from lessons.models import Lesson

# Creates a single pixel black dot gif
small_gif = (b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04'
             b'\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
             b'\x02\x44\x01\x00\x3b')


class TestCreateLessonView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.lesson = Lesson.objects.get(lesson_name='B Lesson')

    def test_logged_out(self):
        '''
        Logged out users will be redirect to login page
        '''
        response = self.client.get(
            '/lessons/create_lesson/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(
            response, '/accounts/login/?next=/lessons/create_lesson/')
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

        response = self.client.get('/lessons/create_lesson/',
                                   follow=True)

        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/')
        self.assertContains(response, 'Only instructors can do this.')

    def test_instructor_get_request(self):
        '''
        A get request by a valid instructor will take
        the instructor to create_lesson.html
        '''
        profile = UserProfile.objects.get(user__username='instructor_1')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            '/lessons/create_lesson', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/create_lesson.html')

    def test_post_valid_form(self):
        '''
        If users is instructor and passes a valid
        form a lesson will be created and instructor
        is redirected to instructor_admin
        '''
        profile = UserProfile.objects.get(user__username='instructor_1')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.post(
            '/lessons/create_lesson/',
            {'lesson_name': 'New Lesson',
             'card_description': 'New Card',
             'description': 'New Description',
             'image': SimpleUploadedFile('small.gif',
                                         small_gif,
                                         content_type='image/gif'),
             'video_url': 'https://www.new',
             'time': '99',
             'price': '99.99'},
            follow=True)

        self.assertTrue(response, 200)
        self.assertRedirects(response, '/lessons/instructor_admin/')

        created_lesson = Lesson.objects.get(lesson_name='New Lesson')
        self.assertEqual(created_lesson.lesson_name, 'New Lesson')
        self.assertEqual(created_lesson.card_description, 'New Card')
        self.assertEqual(created_lesson.description, 'New Description')
        self.assertEqual(created_lesson.video_url, 'https://www.new')
        self.assertEqual(created_lesson.time, 99)
        self.assertAlmostEqual(created_lesson.price, Decimal(99.99))

    def test_invalid_post_data(self):
        '''
        Invalid post data redirects user back to
        instructoradmin with an error message
        '''
        profile = UserProfile.objects.get(user__username='instructor_1')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.post(
            '/lessons/create_lesson/',
            {'lesson_name': 'New Lesson',
             'card_description': 'New Card',
             'description': 'New Description',
             'image': SimpleUploadedFile('small.gif',
                                         small_gif,
                                         content_type='image/gif'),
             'video_url': 'NOT_A_URL',
             'time': '99',
             'price': '99.99'},
            follow=True)

        self.assertTrue(response, 200)
        self.assertRedirects(response, '/lessons/instructor_admin/')

        updated_lesson = Lesson.objects.get(lesson_name='B Lesson')
        self.assertNotEqual(updated_lesson.description,
                            'Updated from a form with bad price data')
        self.assertNotEqual(updated_lesson.price, 'INVALID_PRICE_FOR_FORM')
        self.assertContains(response, ('Invalid form data, please try again. '
                                       'No lesson was created.'))

    def test_create_duplicate_lesson_name(self):
        '''
        If a user creates a lesson with a duplicated name
        from their own created lessons receive an error
        message and redirect to instructor admin page
        '''
        # Login and check lesson exists
        profile = UserProfile.objects.get(user__username='instructor_1')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        self.assertTrue(Lesson.objects.filter(lesson_name='A Lesson').exists())

        # Create a lesson with the same name as above
        response = self.client.post(
            '/lessons/create_lesson/',
            {'lesson_name': 'A Lesson',
             'card_description': 'New Card',
             'description': 'New Description',
             'image': SimpleUploadedFile('small.gif',
                                         small_gif,
                                         content_type='image/gif'),
             'video_url': 'https://www.new',
             'time': '99',
             'price': '99.99'},
            follow=True)

        self.assertRedirects(response,
                             expected_url=reverse('instructor_admin'),
                             status_code=302,
                             target_status_code=200)
        self.assertTemplateUsed(response, 'lessons/instructor_admin.html')

        self.assertContains(response, 'You already have a lesson named this.')
