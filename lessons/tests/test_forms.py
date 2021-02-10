from django.test import TestCase
from lessons.forms import LessonForm, ReviewForm


class TestLessonForm(TestCase):

    def test_lesson_name__is_required(self):
        form = LessonForm({'lesson_name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn(form.errors.keys(), 'name')
        self.assertEqual((form.errors['name'][0], 'This field is required.'))

    def test_fields_are_explicit_in_form_metaclass(self):
        # Check that only the fields we want are visible
        form = LessonForm()
        self.assertEqual(form.Meta.fields, ['lesson_name'])