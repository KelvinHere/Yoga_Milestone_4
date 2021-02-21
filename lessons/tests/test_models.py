from django.test import TestCase
from profiles.models import UserProfile
from lessons.models import (Lesson,
                            Subscription,
                            LessonReview,
                            LessonReviewFlagged)


class TestLessonModels(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

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
