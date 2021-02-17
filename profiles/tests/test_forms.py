from django.test import TestCase, Client

from profiles.models import UserProfile
from profiles.forms import ProfileForm


class TestProfileForm(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def setUp(self):
        self.client = Client()

    def test_form_student_has_instructor_card_description_hidden(self):
        '''
        An instructors card description text
        input is hidden for students
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        form = ProfileForm(instance=profile)
        form_string = str(form)
        self.assertIn('type="hidden" name="card_description"', form_string)

    def test_form_instructor_has_instructor_card_description_visible(self):
        '''
        An instructors card description text
        input is visible for instructors
        '''
        profile = UserProfile.objects.get(user__username='instructor_1')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        form = ProfileForm(instance=profile)
        form_string = str(form)
        self.assertNotIn('type="hidden" name="card_description"', form_string)

    def test_form_instructor_placeholder_change(self):
        '''
        Test profile description and card description
        placeholder tailored to instructor if user is instructor
        '''
        profile = UserProfile.objects.get(user__username='instructor_1')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        form = ProfileForm(instance=profile)
        self.assertEqual(
            form.fields['profile_description'].widget.attrs['placeholder'],
            ('This is displayed as a header above your lessons when a user '
             'enters your studio.'))
        self.assertEqual(
            form.fields['card_description'].widget.attrs['placeholder'],
            ('This will be shown on your instructor card, when users '
             'search for instructors.'))

    def test_form_student_profile_description_placeholder_change(self):
        '''
        Test profile description placeholder tailored
        to student if user is student
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        form = ProfileForm(instance=profile)
        self.assertEqual(
            form.fields['profile_description'].widget.attrs['placeholder'],
            ('Optional for students: Something about you.\n'
             'Required for instructors: About yourself and studio.'))

    def test_form_student_labels(self):
        '''
        Test labels are tailored
        to student if user is student
        '''
        profile = UserProfile.objects.get(user__username='complete_user')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        form = ProfileForm(instance=profile)
        self.assertEqual(
            form.fields['profile_description'].label,
            ('About You'))

    def test_form_instructor_labels(self):
        '''
        Test labels are tailored
        to instructor if user is instructor
        '''
        profile = UserProfile.objects.get(user__username='instructor_1')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        form = ProfileForm(instance=profile)
        self.assertEqual(
            form.fields['profile_description'].label,
            ('Instructor Studio Info'))

    def test_fields_are_explicit_in_metaclass(self):
        '''
        Check fields are explicit to prevent
        unwanted fields and data in form
        '''
        profile = UserProfile.objects.get(user__username='instructor_1')
        login_successful = self.client.login(username=profile.user.username,
                                             password='orange99')
        self.assertTrue(login_successful)

        form = ProfileForm(instance=profile)
        self.assertEqual(form.Meta.fields, ['first_name',
                                            'last_name',
                                            'card_description',
                                            'profile_description',
                                            'image',
                                            ])