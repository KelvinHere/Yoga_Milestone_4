from django.test import TestCase

from checkout.models import OrderLineItem
from profiles.models import UserProfile
from lessons.models import Lesson

class TestCheckoutViews(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        # Login
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)
        # Remove previous purchases
        OrderLineItem.objects.all().delete()
    
    def test_checkout(self):
        # Add items
        lesson = Lesson.objects.get(lesson_name='B Lesson')
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertTrue(response.status_code, 200)

        lesson = Lesson.objects.get(lesson_name='Z Lesson')
        response = self.client.post('/basket/add_to_basket/',
                                    {'lesson_id': lesson.lesson_id},
                                    follow=True)
        self.assertTrue(response.status_code, 200)

        # Check basket has both items
        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        self.assertContains(response, 'B Lesson')
        self.assertContains(response, 'Z Lesson')

        # Checkout
        response = 
    
