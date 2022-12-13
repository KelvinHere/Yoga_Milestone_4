from django.test import TestCase


class TestIndexView(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def test_logged_in_as_instructor(self):
        '''
        Logging in gives success message
        '''
        login_successful = self.client.login(username='instructor_1',
                                             password='orange99')
        self.assertTrue(login_successful)

        response = self.client.get('/', follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, 'id="instructor_admin_frontpage_button"')
        self.assertContains(
            response,
            ('Breathe deep <strong>Instructor_1</strong> and continue your '
             'Yoga journey'))
