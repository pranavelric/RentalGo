from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from .models import KycModel

class UserForm(UserCreationForm):
    class Meta:
        fields = ('first_name','last_name','email','username','password1','password2')
        model = get_user_model()

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email'
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class KycForm(forms.ModelForm):
    class Meta:
        model = KycModel
        fields = ('p_address','curr_address','delivery_address','primary_contact','secondary_contact')
        labels = {
                    'p_address':'Permanent Address Proof (Voter ID / DL / Passport / Aadhaar)',
                    'curr_address': 'Current Address (Rent agreement if not owner)',
                    'primary_contact': 'Primary Contact Number',
                    'secondary_contact': 'Secondary Contact Number',
                    'delivery_address': 'Delivery Address',
        }
