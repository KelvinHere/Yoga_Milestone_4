from django.test import TestCase

from lessons.models import Subscription



class TestIndexView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def test_logged_out(self):
        '''
        Logged out users sent to home page
        with a message and find instructor
        button
        '''
        response = self.client.get('/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, 'Find an instructor')
        self.assertContains(
            response,
            'Breathe deep and begin your Yoga journey here')

    def test_logged_in_normal_user_no_subscriptions(self):
        '''
        Normal users without subscriptions are logged in are sent
        to home page with:-
        - A personalised message
        - Find instructor button
        '''
        # Remove all subscriptions
        Subscription.objects.all().delete()

        login_successful = self.client.login(username='complete_user',
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get('/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, 'Find an instructor')
        self.assertContains(
            response,
            'Breathe deep <strong>Complete_User</strong> and continue your Yoga journey')

    def test_logged_in_normal_user_with_subscriptions(self):
        '''
        Normal users with subscriptions are logged in are sent
        to home page with:-
        - A personalised message
        - Your Subscribed Lessons Button
        '''
        login_successful = self.client.login(username='complete_user',
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get('/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, 'Your Subscribed Lessons')
        self.assertContains(
            response,
            'Breathe deep <strong>Complete_User</strong> and continue your Yoga journey')
