from django.test import TestCase
from django.conf import settings


class TestInfoView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def test_info_page(self):
        '''
        This page can be accessed
        while logged out and uses
        settings.py to display the
        current email
        '''
        response = self.client.get('/info/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/info.html')
        self.assertContains(response, ('Welcome to Social Yoga, here you will '
                                       'find a place to practice and enjoy '
                                       'quality Yoga sessions'))

    def test_info_page_email_is_correct(self):
        '''
        Test email is pulled correctly
        from settings.py
        '''
        response = self.client.get('/info/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/info.html')
        self.assertContains(response, settings.DEFAULT_FROM_EMAIL)
