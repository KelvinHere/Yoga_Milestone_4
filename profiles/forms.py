from django import forms
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    """ A form for Profiles """

    class Meta:
        model = UserProfile
        fields = '__all__'

    # Over-ride init
    def __init__(self, *args, **kwargs): 
        super(ProfileForm, self).__init__(*args, **kwargs)  
        #instructor_profile = forms.CharField(widget=forms.HiddenInput())
        self.fields['user'].disabled = True
        self.fields['is_instructor'].disabled = True
