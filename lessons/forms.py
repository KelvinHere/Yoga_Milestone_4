from django import forms
from .widgets import CustomClearableFileInput
from .models import Lesson, LessonReview


class LessonForm(forms.ModelForm):
    """ A form for the 'Create Lesson' page """

    class Meta:
        model = Lesson
        fields = ['lesson_name',
                  'card_description',
                  'description',
                  'image',
                  'video_url',
                  'time',
                  'price',
                  ]

        image = forms.ImageField(label='Image',
                                 required=True,
                                 widget=CustomClearableFileInput)

        labels = {
            'card_description': 'Short Description for lesson card',
            'description': 'Lesson Description',
            'time': 'Length of lesson in minutes',
            'price': 'Lesson price (EUR), leave 0 for free',
            'video_url': 'Embedded video URL',
        }

    # Over-ride init
    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields['card_description'].widget = forms.Textarea(attrs={
            'rows': 3,
            'cols': 25,
            'maxlength': 254
            })

        # Add styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'custom-crispy-form-styling'


class ReviewForm(forms.ModelForm):
    """ A review form """
    RATING_CHOICES = (
        ('', 'Choose a rating out of 10'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'), )

    rating_dropdown = forms.ChoiceField(choices=RATING_CHOICES,
                                        label="Rating out of 10")

    class Meta:
        model = LessonReview
        fields = '__all__'
        widgets = {'profile': forms.HiddenInput,
                   'lesson': forms.HiddenInput,
                   'date': forms.HiddenInput,
                   'rating': forms.HiddenInput, }

    # Over-ride init
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        # Add styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'custom-crispy-form-styling'
