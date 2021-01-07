from django import forms
from .models import Lesson


class LessonForm(forms.ModelForm):
    """ A form for the 'Create Lesson' page """

    class Meta:
        model = Lesson
        fields = '__all__'

    # Over-ride init
    def __init__(self, *args, **kwargs): 
        super(LessonForm, self).__init__(*args, **kwargs)  
        #instructor_profile = forms.CharField(widget=forms.HiddenInput())
        self.fields['instructor_profile'].disabled = True 
