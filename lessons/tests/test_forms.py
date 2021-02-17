from django.test import TestCase
from lessons.forms import LessonForm, ReviewForm


class TestLessonForm(TestCase):

    def test_lesson_name_is_required(self):
        form = LessonForm({'lesson_name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('lesson_name', form.errors.keys())
        self.assertEqual(form.errors['lesson_name'][0],
                         'This field is required.')

    def test_description_is_required(self):
        form = LessonForm({'description': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors.keys())
        self.assertEqual(form.errors['description'][0],
                         'This field is required.')

    def test_card_description_is_required(self):
        form = LessonForm({'card_description': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('card_description', form.errors.keys())
        self.assertEqual(form.errors['card_description'][0],
                         'This field is required.')

    def test_image_required(self):
        form = LessonForm({'image': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors.keys())
        self.assertEqual(form.errors['image'][0],
                         'This field is required.')

    def test_video_url_required(self):
        form = LessonForm({'video_url': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('video_url', form.errors.keys())
        self.assertEqual(form.errors['video_url'][0],
                         'This field is required.')

    def test_time_required(self):
        form = LessonForm({'time': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('time', form.errors.keys())
        self.assertEqual(form.errors['time'][0],
                         'This field is required.')

    def test_price_required(self):
        form = LessonForm({'price': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors.keys())
        self.assertEqual(form.errors['price'][0],
                         'This field is required.')

    def test_fields_are_explicit_in_metaclass(self):
        form = LessonForm()
        self.assertEqual(form.Meta.fields, ['lesson_name',
                                            'card_description',
                                            'description',
                                            'image',
                                            'video_url',
                                            'time',
                                            'price',
                                            ])


class TestReviewForm(TestCase):

    def test_review_required(self):
        form = ReviewForm({'review': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('review', form.errors.keys())
        self.assertEqual(form.errors['review'][0],
                         'This field is required.')

    def test_rating_required(self):
        form = ReviewForm({'rating': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors.keys())
        self.assertEqual(form.errors['rating'][0],
                         'This field is required.')

    def test_fields_hidden_fields(self):
        '''
        Test that hidden fields widget is
        applied to appropriate fields
        '''
        form = ReviewForm()

        self.assertIn(
            'django.forms.widgets.HiddenInput',
            str(form.fields['profile'].widget))

        self.assertIn(
            'django.forms.widgets.HiddenInput',
            str(form.fields['lesson'].widget))

        self.assertIn(
            'django.forms.widgets.HiddenInput',
            str(form.fields['date'].widget))

        self.assertIn(
            'django.forms.widgets.HiddenInput',
            str(form.fields['rating'].widget))
