from django.test import TestCase

from datetime import datetime

from profiles.models import UserProfile
from lessons.models import LessonReview, Lesson


class TestProfileModels(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def test_user_profile_update_rating(self):
        '''
        Reviews affect overall lesson score
        Average of all lessons is instructor score
        Test adding review feeds all the way to instructor rating
        '''
        # Remove all reviews
        LessonReview.objects.all().delete()

        lesson = Lesson.objects.get(lesson_name='H Lesson')
        instructor = lesson.instructor_profile
        reviewer1 = UserProfile.objects.get(user__username='complete_user')
        reviewer2 = UserProfile.objects.get(user__username='incomplete_user')

        # Post a 10 star review on this lesson
        LessonReview.objects.create(profile=reviewer1,
                                    lesson=lesson,
                                    review="My review",
                                    rating=10,
                                    date=datetime.now())

        # Instructor rating is 10
        self.assertTrue(instructor.rating, 10)

        # Post a 2 star review on this lesson
        LessonReview.objects.create(profile=reviewer2,
                                    lesson=lesson,
                                    review="My review",
                                    rating=2,
                                    date=datetime.now())

        # Instructor rating is < 10
        self.assertLess(instructor.rating, 10)

    def test_user_profile_rating_resets_to_none_when_no_reviews_exist(self):
        '''
        If all reviews are removed instructors
        UserProfile rating resets to None
        '''
        instructor = UserProfile.objects.get(user__username='instructor_1')

        # Instructor has a 1 to 10 rating
        self.assertTrue(instructor.rating in range(1, 11))

        # Remove all reviews
        LessonReview.objects.all().delete()

        # Instructor has rating value of None
        self.assertTrue(instructor.rating, None)

    def test_user_profile_rating_resets_to_none_when_no_lessons_exist(self):
        '''
        If all lessons are removed for an instructor
        the rating returns to None
        '''
        instructor = UserProfile.objects.get(user__username='instructor_1')
        lessons = Lesson.objects.filter(instructor_profile=instructor)

        # Loop to allow signal to fire, does not work on bulk delete
        for lesson in lessons:
            lesson.delete()
        self.assertTrue(instructor.rating, None)
