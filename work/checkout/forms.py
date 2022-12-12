from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email')
        labels = {
            'full_name': 'Full Name ',
            'email': 'Email Address '
        }

    def __init__(self, *args, **kwargs):
        """ Format form """
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
