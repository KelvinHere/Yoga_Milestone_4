from django.test import TestCase
from django.shortcuts import reverse
from datetime import datetime

from profiles.models import UserProfile
from lessons.models import Lesson, LessonReview


class TestReviewLessonView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.free_lesson = Lesson.objects.filter(is_free=True).first()
        self.invalid_lesson_id = "SDFGGRFVAD"
        self.complete_user = {'username': 'complete_user',
                              'password': 'orange99'}

    def test_logged_out(self):
        ''' Logged out users will be redirect to login page '''

        response = self.client.get(
            f'/lessons/review_lesson/{self.free_lesson.lesson_id}',
            follow=True)

        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response,
                             ('/accounts/login/?next=/lessons/review_'
                              f'lesson/{self.free_lesson.lesson_id}'))
        self.assertContains(response,
                            ('If you have not created an account yet,'
                             ' then please'))

    def test_edit_existing_review_get(self):
        '''
        GET request, existing review redirects user
        to a pre-filled review form
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(
            username=self.complete_user['username'],
            password=self.complete_user['password'])
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/lessons/review_lesson/{self.free_lesson.lesson_id}',
            follow=True)

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/review.html')
        self.assertContains(response, 'Review for "A Lesson"')
        self.assertContains(response, 'Review by complete_user')
        self.assertContains(response, 'Great I loved it!')
        self.assertTrue(
            LessonReview.objects.filter(lesson=self.free_lesson,
                                        profile=profile).exists())

    def test_no_existing_review_get(self):
        '''
        GET request, no existing review redirects
        user to a blank review form
        '''
        lesson = Lesson.objects.get(lesson_name='Z Lesson')
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/lessons/review_lesson/{lesson.lesson_id}',
            follow=True)

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/review.html')
        self.assertContains(response, 'Review for "Z Lesson"')
        self.assertContains(response, 'Review by complete_user')
        self.assertFalse(
            LessonReview.objects.filter(lesson=lesson,
                                        profile=profile).exists())

    def test_invalid_lesson_id(self):
        '''
        Invalid lesson id sends user to home page
        with an error message
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/lessons/review_lesson/{self.invalid_lesson_id}',
            follow=True)

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, ('Cannot create/edit a review for an '
                                       'invalid lesson'))

    def test_invalid_form(self):
        '''
        Invalid form sends user back to lesson
        page with an error message
        '''
        profile = UserProfile.objects.get(user__username='incomplete_user')
        lesson = Lesson.objects.get(lesson_name='H Lesson')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.post(
            f'/lessons/review_lesson/{lesson.lesson_id}',
            {"id": 1,
             "profile": profile.id,
             "lesson": lesson.id,
             "review": ("Error line too long, Error line too long, ") * 500,
             "rating_dropdown": 5,
             "date": datetime.now()},
            follow=True)

        self.assertRedirects(response, f'/studio/{lesson.lesson_id}/')
        self.assertContains(response, ('Error in review form:'))
        # No review created
        self.assertFalse(
            LessonReview.objects.filter(lesson=lesson,
                                        profile=profile).exists())

    def test_cant_review_your_own_lesson(self):
        '''
        Instructors trying to review their own lessons are
        redirected back to studo page with error message.
        '''
        lesson = Lesson.objects.get(lesson_name='A Lesson')
        login_successful = self.client.login(username='instructor_1',
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/lessons/review_lesson/{lesson.lesson_id}',
            follow=True)

        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, f'/studio/{lesson.lesson_id}/')
        self.assertTemplateUsed(response, 'studio/studio.html')
        self.assertContains(response, 'You cannot review your own lessons.')

    def test_update_review_post(self):
        '''
        Update an existing review
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        lesson = Lesson.objects.get(lesson_name='Y Lesson')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.post(
            f'/lessons/review_lesson/{lesson.lesson_id}',
            {"id": 1,
             "profile": profile.id,
             "lesson": lesson.id,
             "review": "I have been updated",
             "rating_dropdown": 5,
             "date": datetime.now()},
            follow=True)

        self.assertRedirects(response, f'/studio/{lesson.lesson_id}/')
        self.assertContains(response, 'I have been updated')
        self.assertTrue(
            LessonReview.objects.filter(lesson=lesson,
                                        profile=profile).exists())

    def test_create_review_post(self):
        '''
        Post a review where there previously was none
        '''
        profile = UserProfile.objects.get(user__username='incomplete_user')
        lesson = Lesson.objects.get(lesson_name='H Lesson')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.post(
            f'/lessons/review_lesson/{lesson.lesson_id}',
            {"id": 1,
             "profile": profile.id,
             "lesson": lesson.id,
             "review": "I am a new review that has just been created",
             "rating_dropdown": 5,
             "date": datetime.now()},
            follow=True)

        self.assertRedirects(response, f'/studio/{lesson.lesson_id}/')
        self.assertContains(response, ('I am a new review that has just '
                                       'been created'))
        self.assertTrue(
            LessonReview.objects.filter(lesson=lesson,
                                        profile=profile).exists())

    def test_cant_create_review_on_lesson_not_owned_post(self):
        '''
        User cannot post review on lesson they do not own
        '''
        lesson = Lesson.objects.get(lesson_name='Z Lesson')
        profile = UserProfile.objects.get(user__username='incomplete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        self.assertFalse(
            LessonReview.objects.filter(lesson=lesson,
                                        profile=profile).exists())

        response = self.client.post(
            f'/lessons/review_lesson/{lesson.lesson_id}',
            {"id": 1,
             "profile": lesson.id,
             "lesson": profile.id,
             "review": "I tried to post on a paid lesson I do not own",
             "rating_dropdown": 5,
             "date": datetime.now()},
            follow=True)

        self.assertRedirects(response,
                             expected_url=reverse('home'),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(response, ('You cannot review a lesson you '
                                       'do not own.'))
        self.assertFalse(
            LessonReview.objects.filter(lesson=lesson,
                                        profile=profile).exists())

    def test_stop_user_spoofing_profile_in_form(self):
        '''
        User cannot create / update / a review created
        by another users profile
        '''
        profile = UserProfile.objects.get(user__username='incomplete_user')

        another_profile = UserProfile.objects.get(
            user__username='complete_user')

        lesson = Lesson.objects.get(lesson_name='H Lesson')

        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.post(
            f'/lessons/review_lesson/{lesson.lesson_id}',
            {"id": 1,
             "profile": another_profile.id,
             "lesson": lesson.id,
             "review": "I am a new review that has just been created",
             "rating_dropdown": 5,
             "date": datetime.now()},
            follow=True)

        self.assertRedirects(response, f'/studio/{lesson.lesson_id}/')
        self.assertContains(response, ('You can only create and edit your '
                                       'own reviews.'))

    def test_rating_too_high(self):
        '''
        Test rating too high
        Review rating has to be from 1 to 10
        '''
        invalid_lesson_rating = 11
        profile = UserProfile.objects.get(user__username='incomplete_user')
        lesson = Lesson.objects.get(lesson_name='H Lesson')
        lesson_id = lesson.lesson_id
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.post(
            f'/lessons/review_lesson/{lesson.lesson_id}',
            {"id": 1,
             "profile": profile.id,
             "lesson": lesson.id,
             "review": "I am a new review that has just been created",
             "rating_dropdown": invalid_lesson_rating,
             "date": datetime.now()},
            follow=True)

        self.assertRedirects(response, f'/studio/{lesson_id}/')
        self.assertContains(response, ('You entered an invalid rating, please '
                                       'try again.'))
        self.assertFalse(
            LessonReview.objects.filter(lesson=lesson,
                                        profile=profile).exists())

    def test_rating_too_low(self):
        '''
        Test rating too low
        Review rating has to be from 1 to 10
        '''
        invalid_lesson_rating = -1
        profile = UserProfile.objects.get(user__username='incomplete_user')
        lesson = Lesson.objects.get(lesson_name='H Lesson')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        response = self.client.post(
            f'/lessons/review_lesson/{lesson.lesson_id}',
            {"id": 1,
             "profile": profile.id,
             "lesson": lesson.id,
             "review": "I am a new review that has just been created",
             "rating_dropdown": invalid_lesson_rating,
             "date": datetime.now()},
            follow=True)

        self.assertRedirects(response, f'/studio/{lesson.lesson_id}/')
        self.assertContains(response, ('You entered an invalid rating, please '
                                       'try again.'))
        self.assertFalse(
            LessonReview.objects.filter(lesson=lesson,
                                        profile=profile).exists())

    def test_rating_euqals_none_if_all_reviews_deleted(self):
        '''
        If all reviews are deleted the lessons
        rating should return to None even if
        reviews are deleted from Django admin
        '''
        # Lesson exists with a valid integer rating
        lesson = Lesson.objects.get(lesson_name="A Lesson")
        self.assertTrue(lesson.rating in range(1, 11))

        # Lesson rating returns to None
        LessonReview.objects.all().delete()
        self.assertTrue(lesson.rating, None)

    def test_rating_changed_when_review_added(self):
        '''
        The lesson rating changes
        when a review is added
        '''
        # Old Lesson has one 10 star review
        lesson = Lesson.objects.get(lesson_name='H Lesson')
        self.assertTrue(lesson.rating, 10)

        profile = UserProfile.objects.get(user__username='incomplete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        # Give lesson an 8 star review
        response = self.client.post(
            f'/lessons/review_lesson/{lesson.lesson_id}',
            {"id": 1,
             "profile": profile.id,
             "lesson": lesson.id,
             "review": "I am a new review that has just been created",
             "rating_dropdown": 8,
             "date": datetime.now()},
            follow=True)

        self.assertTrue(response.status_code, 200)

        # New review will equal 9
        lesson = Lesson.objects.get(lesson_name='H Lesson')
        new_rating = lesson.rating
        self.assertAlmostEquals(new_rating, 9)
