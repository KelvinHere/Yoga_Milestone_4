from django import forms
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
            'description': 'Text under video',
            'time': 'Estimated length of lesson',
        }

    # Over-ride init
    def __init__(self, *args, **kwargs): 
        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields['instructor_profile'].disabled = True
        self.fields['rating'].disabled = True
        self.fields['card_description'].widget = forms.Textarea(attrs={'rows': 3, 'cols': 25, 'maxlength': 254})

        # Add styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'custom-crispy-form-styling'


class ReviewForm(forms.ModelForm):
    """ A review form """

    class Meta:
        model = LessonReview
        fields = '__all__'
        widgets = {'profile': forms.HiddenInput,
                   'lesson': forms.HiddenInput,
        }

    # Over-ride init
    def __init__(self, *args, **kwargs): 
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['profile'].disabled = True
        self.fields['lesson'].disabled = True

        # Add styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'custom-crispy-form-styling'