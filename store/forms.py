# forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):

    #hide usable password options
    usable_password = None

    class Meta:
        model = User
         # Fields from User model to be included in the form
        fields = ['username','email', 'first_name', 'last_name', 'password1', 'password2']
