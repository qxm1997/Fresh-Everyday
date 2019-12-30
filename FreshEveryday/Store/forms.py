from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class UserForm(forms.Form):
    firstname = forms.CharField(min_length=2, max_length=12)
    lastname = forms.CharField(min_length=1, max_length=6)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, validators=[
        RegexValidator(regex="^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$", message='密码至少包含 数字和英文，长度6-20')])
