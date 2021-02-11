from django.test import TestCase
from django.contrib.auth.models import User

from lessons.models import Lesson
from profiles.models import UserProfile

from decimal import Decimal



class TestLessonViews(TestCase):

    def setup(self):
        # Create instructor
        instructor = UserProfile.objects.create(
            id=2,
            user_id=2,
            first_name='Benny',
            last_name='Lee',
            is_instructor=True,
            requested_instructor_status=True,
            card_description='',
            profile_description='I love teaching Yoga, come join me!',
            image='profile_images/instructor_4.jpeg',
            rating=None,
            lesson_count=1
        )
        instructor.save()

        # Create lesson
        '''
        lesson = Lesson.objects.create(
            id=1,
            lesson_id='1CF0AF7475FE46BD84C0A4A8DDCF2DD6',
            instructor_profile_id=2,
            lesson_name='Sun Salutation',
            card_description='Sun salutation',
            description='Test Lesson main description',
            image='lesson_images/sunsalutation.jpeg',
            rating=10,
            video_url='https://www.youtube.com/embed/dqAQ26_GRV4',
            time=10,
            is_free=True,
            price=0.00
        )
        lesson.save()
        '''

    def test_get_lessons(self):
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/lessons.html')

    def test_lessons_with_valid_instructor_filter(self):
        print(self.instructor)
        response = self.client.get('/lessons', {'instructor': self.instructor['id']})
        # self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, 'instructors')

     #   print('######')
      #  print(response)
        #self.assertEqual(response.status_code, 200)


    #def test_post_to_subscribe_view_when_not_logged_in(self):
    #    response = self.client.get('/lessons/subscriptions?subscribe=false&lesson_id=1CF0AF7475FE46BD84C0A4A8DDCF2DD6')
    #    self.assertRedirects(response, '/accounts/login/?next=/lessons/subscriptions/')

    #def test_subscibe_to_lesson(self):
    #    self.client.force_login(User.objects.get_or_create(username='testuser')[0])
    #    response = self.client.post('/lessons/subscriptions/', {'subscribe': 'True', 'id': '1CF0AF7475FE46BD84C0A4A8DDCF2DD6'})
    #    print(response)
    #    print('######')
    #    self.assertEqual(response.status_code, 200)
