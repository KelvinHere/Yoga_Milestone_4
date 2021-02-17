from django.test import TestCase


class TestProfileForm(TestCase):

    def test_form_method_profile_is_complete_false(self):
        '''
        An incomplete profile should