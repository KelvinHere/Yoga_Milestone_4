from django import forms
from .models import Lesson


class CreateLessonForm(forms.ModelForm):
    """ A form for the 'Create Lesson' page """

    class Meta:
        model = Lesson
        fields = '__all__'

    # Over-ride init
    def __init__(self, *args, **kwargs): 
        super(CreateLessonForm, self).__init__(*args, **kwargs)  
        #instructor_name = forms.CharField(widget=forms.HiddenInput())
        self.fields['instructor_name'].disabled = True 
