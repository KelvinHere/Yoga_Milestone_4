from django import forms
from .widgets import CustomClearableFileInput
from .models import Lesson, LessonReview


class LessonForm(forms.ModelForm):
    """ A form for the 'Create Lesson' page """

    class Meta:
        model = Lesson
        fields = '__all__'
        widgets = {'instructor_profile': forms.HiddenInput,
                   'rating': forms.HiddenInput,
        }
        labels = {
            'card_description': 'Description for lesson card',
            'description': 'Large description',
            'time': 'Estimated length of lesson',
        }

        image = forms.ImageField(label='image',
                                 required=False,
                                 widget=CustomClearableFileInput)

    # Over-ride init
    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields['instructor_profile'].disabled = True
        self.fields['rating'].disabled = True
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
        (10, '10'),
    )
    rating_dropdown = forms.ChoiceField(choices=RATING_CHOICES,
                                        label="Rating out of 10")

    class Meta:
        model = LessonReview
        fields = '__all__'
        widgets = {'profile': forms.HiddenInput,
                   'lesson': forms.HiddenInput,
                   'date': forms.HiddenInput,
                   'rating': forms.HiddenInput,
        }

    # Over-ride init
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        # Add styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'custom-crispy-form-styling'
