from django.test import TestCase

from checkout.forms import OrderForm


class TestOrderForm(TestCase):

    def test_full_name_required(self):
        form = OrderForm({'full_name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors.keys())
        self.assertEqual(form.errors['full_name'][0],
                         'This field is required.')

    def test_email_required(self):
        form = OrderForm({'email': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())
        self.assertEqual(form.errors['email'][0],
                         'This field is required.')

    def test_fields_are_explicit_in_metaclass(self):
        form = OrderForm()
        self.assertEqual(form.Meta.fields, ('full_name', 'email'))
