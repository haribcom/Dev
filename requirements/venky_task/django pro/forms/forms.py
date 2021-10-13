from django import forms
from django.contrib.auth.models import User
from hrb.models import urequests
class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name']
class bookroom(forms.ModelForm):
    class Meta:
        model=urequests
        fields='__all__'
