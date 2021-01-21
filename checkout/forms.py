from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email')

    def __init__(self, *args, **kwargs):
        """ Format form """
        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name*',
            'email': 'Email Address*'
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholders'] = placeholder
            self.fields[field].label = False