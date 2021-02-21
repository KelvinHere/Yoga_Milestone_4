from django.test import TestCase

from django.test import TestCase
from profiles.models import UserProfile
from lessons.models import (Lesson,
                            Subscription,
                            LessonReview,
                            LessonReviewFlagged)


class TestLessonModels(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.instructor_profile = UserProfile.objects.get(
            user__username='instructor_1')

    def test_lesson_price_defaults_to_zero(self):
        test_lesson = Lesson.objects.create(
                        instructor_profile=self.instructor_profile,
                        lesson_name='Test Lesson',
                        card_description='Test Card Description',
                        description='Test Description',
                        image='lesson_images/test.jpg',
                        video_url='https://www.test',
                        time=10, )

        self.assertEqual(test_lesson.price, 0.00)

    def test_lesson_id_uuid_created(self):
        test_lesson = Lesson.objects.create(
                        instructor_profile=self.instructor_profile,
                        lesson_name='Test Lesson',
                        card_description='Test Card Description',
                        description='Test Description',
                        image='lesson_images/test.jpg',
                        video_url='https://www.test',
                        time=10, )

        self.assertNotEqual(test_lesson.lesson_id, '')

    def test_lesson_is_free_defaults_to_true_when_price_is_zero(self):
        test_lesson = Lesson.objects.create(
                        instructor_profile=self.instructor_profile,
                        lesson_name='Test Lesson',
                        card_description='Test Card Description',
                        description='Test Description',
                        image='lesson_images/test.jpg',
                        video_url='https://www.test',
                        time=10,
                        price=0.00, )

        self.assertEqual(test_lesson.is_free, True)

    def test_is_free_defaults_to_false_when_price_is_not_zero(self):
        test_lesson = Lesson.objects.create(
                        instructor_profile=self.instructor_profile,
                        lesson_name='Test Lesson',
                        card_description='Test Card Description',
                        description='Test Description',
                        image='lesson_images/test.jpg',
                        video_url='https://www.test',
                        time=10,
                        price=9.99, )

        self.assertEqual(test_lesson.is_free, False)

    def test_lesson_str(self):
        lesson = Lesson.objects.filter().first()
        self.assertEqual(str(lesson), lesson.lesson_name)

    def test_lesson_get_instructor_profile(self):
        lesson = Lesson.objects.filter().first()
        profile = lesson.instructor_profile
        self.assertEqual(profile, lesson.get_instructor_profile())

    def test_subscription_str(self):
        sub = Subscription.objects.filter().first()
        self.assertEqual(str(sub), (f'Lesson "{sub.lesson.lesson_name}" '
                                    f'subscribed to by "{sub.user}"'))

    def test_lessonreview_str(self):
        review = LessonReview.objects.filter().first()
        self.assertEqual(str(review),
                         (f'Review of "{review.lesson.lesson_name}"'
                          f' by "{review.profile}"'))

    def test_lessonreviewflagged_str(self):
        # Create a flag
        profile = UserProfile.objects.get(user__username='complete_user')
        review = LessonReview.objects.filter().first()
        flag = LessonReviewFlagged.objects.create(profile=profile,
                                                  review=review)
        self.assertEqual(str(flag),
                         (f'Review of "{flag.review.lesson.lesson_name}" '
                          f'flagged by "{flag.profile}"'))
