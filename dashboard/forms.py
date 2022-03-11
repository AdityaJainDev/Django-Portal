from cProfile import label
from urllib import request
from django import forms
from django.utils.translation import gettext_lazy as _


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_('EmailInput'), required = True)

class ChangePassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label=_('OldPassword'))
    new_password = forms.CharField(widget=forms.PasswordInput(), label=_('NewPassword'))
    confirm_password = forms.CharField(widget=forms.PasswordInput(),label=_('ConfirmPassword'))


        