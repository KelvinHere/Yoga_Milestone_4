from django import forms
from .models import Lesson


class LessonForm(forms.ModelForm):
    """ A form for the 'Create Lesson' page """

    class Meta:
        model = Lesson
        fields = '__all__'
        widgets = {'instructor_profile': forms.HiddenInput}

    # Over-ride init
    def __init__(self, *args, **kwargs): 
        super(LessonForm, self).__init__(*args, **kwargs)  
        self.fields['instructor_profile'].disabled = True 
