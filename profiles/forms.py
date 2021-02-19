from django import forms
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    """ A form for Profiles """

    class Meta:
        model = UserProfile
        fields = ['first_name',
                  'last_name',
                  'card_description',
                  'profile_description',
                  'image',
                  ]
        labels = {
            'card_description': 'Instructor card description',
        }

    # Over-ride init
    def __init__(self, *args, **kwargs):
        self.profile = kwargs['instance']
        super(ProfileForm, self).__init__(*args, **kwargs)

        if self.profile.is_instructor:
            profile_description_placeholder = (
                'This is displayed as a header above your lessons '
                'when a user enters your studio.')

            card_desctiption_placeholder = (
                'This will be shown on your instructor card, when users '
                'search for instructors.')

            self.fields['card_description'].widget = forms.Textarea(
                attrs={'rows': 3,
                       'cols': 25,
                       'maxlength': 254,
                       'placeholder': card_desctiption_placeholder}
                )
            self.fields['profile_description'].label = 'Instructor Studio Info'
        else:
            profile_description_placeholder = (
                ('Optional for students: Something about you.\n'
                 'Required for instructors: About yourself and studio.'))

            self.fields['card_description'].widget = forms.HiddenInput()
            self.fields['profile_description'].label = 'About You'

        self.fields['profile_description'].widget = forms.Textarea(
            attrs={'placeholder': profile_description_placeholder}
        )
