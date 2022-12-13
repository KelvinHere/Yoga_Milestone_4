from django.test import TestCase
from django.shortcuts import reverse

from profiles.models import UserProfile
from lessons.models import LessonReview


class TestDeleteReviewView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def test_logged_out(self):
        ''' Logged out users will be redirect to login page '''
        response = self.client.get('/lessons/delete_review/9', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response,
                             '/accounts/login/?next=/lessons/delete_review/9')
        self.assertContains(response, ('If you have not created an account '
                                       'yet, then please'))

    def test_invalid_review(self):
        '''
        Invalid review will redirect user home with
        an error message
        '''
        invalid_review_pk = "ASDFASDFSDAFASDF"
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/lessons/delete_review/{invalid_review_pk}',
            follow=True)

        self.assertRedirects(response,
                             expected_url=reverse('home'),
                             status_code=302,
                             target_status_code=200)
        self.assertContains(response, ('Cannot delete review, review '
                                       'not found.'))

    def test_delete_another_users_review(self):
        '''
        User cannot delete a review they
        did not create
        '''
        # Get profile
        profile = UserProfile.objects.get(user__username='incomplete_user')
        # Get another profile
        another_profile = UserProfile.objects.get(
            user__username='complete_user')

        # Get another profiles review
        another_users_review = LessonReview.objects.filter(
            profile=another_profile).first()

        lesson = another_users_review.lesson

        # Lesson review exists
        self.assertTrue(LessonReview.objects.filter(
            lesson=lesson,
            profile=another_profile).exists())

        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/lessons/delete_review/{another_users_review.id}',
            follow=True)

        self.assertRedirects(
            response,
            expected_url=reverse('studio', args=(lesson.lesson_id,)),
            status_code=302,
            target_status_code=200)
        self.assertContains(response, ('Cannot delete review, it does '
                                       'not belong to this account.'))

        # Lesson review still exists
        self.assertTrue(
            LessonReview.objects.filter(lesson=lesson,
                                        profile=another_profile).exists())

    def test_delete_review_valid_request(self):
        '''
        Deletes a review
        '''
        profile = UserProfile.objects.get(user__username='incomplete_user')
        users_review = LessonReview.objects.filter(profile=profile).first()
        lesson = users_review.lesson

        self.assertTrue(LessonReview.objects.filter(
            lesson=lesson,
            profile=profile).exists())

        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get(
            f'/lessons/delete_review/{users_review.id}',
            follow=True)

        self.assertRedirects(
            response,
            expected_url=reverse('studio', args=(lesson.lesson_id,)),
            status_code=302,
            target_status_code=200)

        self.assertContains(response, 'Review deleted.')
        self.assertFalse(
            LessonReview.objects.filter(lesson=lesson,
                                        profile=profile).exists())

    def test_superuser_delete_review(self):
        '''
        Superuser can delete any review
        '''
        users_review = LessonReview.objects.filter(
            profile__user__username='complete_user').first()

        lesson = users_review.lesson
        profile = users_review.profile
        self.assertTrue(
            LessonReview.objects.filter(lesson=lesson,
                                        profile=profile).exists())

        login_successful = self.client.login(username='kelvinhere',
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.post(
            f'/lessons/delete_review/{users_review.id}',
            follow=True)

        self.assertContains(response, '"success": "True"')
        self.assertFalse(
            LessonReview.objects.filter(lesson=lesson,
                                        profile=profile).exists())
