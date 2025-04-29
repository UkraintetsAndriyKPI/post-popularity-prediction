from django import forms

class PostAttempt(forms.Form):
    url = forms.URLField(
        label='Enter URL',
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://reddit.com/'
        }))
