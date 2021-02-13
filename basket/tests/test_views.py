from django.test import TestCase

from profiles.models import UserProfile
from lessons.models import Subscription, Lesson


class TestBasketViews(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

    def test_logged_out(self):
        ''' Logged out users will be redirect to login page '''
        response = self.client.get('/basket/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, '/accounts/login/?next=/basket')
        self.assertContains(response, html.escape('If you have not created an account yet, then please'))