from django.test import TestCase

from profiles.models import UserProfile
from lessons.models import Lesson


class TestLessonModel(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.instructor_profile = UserProfile.objects.get(
            user__username='instructor_1')

    def test_price_defaults_to_zero(self):
        test_lesson = Lesson.objects.create(
                        instructor_profile=self.instructor_profile,
                        lesson_name='Test Lesson',
                        card_description='Test Card Description',
                        description='Test Description',
                        image='lesson_images/test.jpg',
                        video_url='https://www.test',
                        time=10,
                        )

        self.assertEqual(test_lesson.price, 0.00)

    def test_lesson_id_uuid_created(self):
        test_lesson = Lesson.objects.create(
                        instructor_profile=self.instructor_profile,
                        lesson_name='Test Lesson',
                        card_description='Test Card Description',
                        description='Test Description',
                        image='lesson_images/test.jpg',
                        video_url='https://www.test',
                        time=10,
                        )

        self.assertNotEqual(test_lesson.lesson_id, '')

    def test_is_free_defaults_to_true_when_price_is_zero(self):
        test_lesson = Lesson.objects.create(
                        instructor_profile=self.instructor_profile,
                        lesson_name='Test Lesson',
                        card_description='Test Card Description',
                        description='Test Description',
                        image='lesson_images/test.jpg',
                        video_url='https://www.test',
                        time=10,
                        price=0.00,
                        )

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
                        price=9.99,
                        )

        self.assertEqual(test_lesson.is_free, False)
