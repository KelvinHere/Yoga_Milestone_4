from django import forms
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    """ A form for Profiles """

    class Meta:
        model = UserProfile
        fields = '__all__'
        widgets = {
                   'user': forms.HiddenInput,
                   'is_instructor': forms.HiddenInput,
                   'rating': forms.HiddenInput,
                  }

    # Over-ride init
    def __init__(self, *args, **kwargs): 
        super(ProfileForm, self).__init__(*args, **kwargs)  
        self.fields['user'].disabled = True
        self.fields['is_instructor'].disabled = True
        self.fields['rating'].disabled = True
