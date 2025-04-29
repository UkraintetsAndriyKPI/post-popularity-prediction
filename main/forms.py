import django.forms as forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class UpdateUserForm(UserChangeForm):
    email = forms.EmailField(label="Email", required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="First name", required=False, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="Last name", required=False, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
