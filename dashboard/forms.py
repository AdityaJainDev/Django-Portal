from django import forms
from django.utils.translation import gettext_lazy as _

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_('EmailInput'), required = True)
        