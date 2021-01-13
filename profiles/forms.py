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
            'requested_instructor_status': forms.HiddenInput,
        }
        labels = {
            'card_description': 'Instructor card description'
        }

    # Over-ride init
    def __init__(self, *args, **kwargs): 
        super(ProfileForm, self).__init__(*args, **kwargs)  

        card_desctiption_placeholder = 'A brief description of yourself and ethos (256 characters)'
        self.fields['user'].disabled = True
        self.fields['is_instructor'].disabled = True
        self.fields['rating'].disabled = True
        self.fields['card_description'].widget = forms.Textarea(attrs={'rows': 3, 'cols': 25, 'maxlength': 254, 'placeholder': card_desctiption_placeholder})