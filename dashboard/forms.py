from cProfile import label
from urllib import request
from django import forms
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _

Billing_Details = (
    ("0", _("ByEmail")),
    ("1", _("ByPost")),
    ("2", _("ByFax")),
)


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("EmailInput"), required=True)


class ChangePassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label=_("OldPassword"))
    new_password = forms.CharField(widget=forms.PasswordInput(), label=_("NewPassword"))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), label=_("ConfirmPassword")
    )


class PersonalDataEdit(forms.Form):
    company = forms.CharField(label=_("CompanyName"))
    first_name = forms.CharField(label=_("FirstName"))
    last_name = forms.CharField(label=_("LastName"))
    address = forms.CharField(label=_("Address"))
    postcode = forms.CharField(label=_("Postcode"))
    city = forms.CharField(label=_("City"))
    country = CountryField(blank_label=_("Country")).formfield()
    email = forms.EmailField(label=_("Email"))
    phone = forms.CharField(widget=forms.NumberInput(), label=_("Phone"))
    fax = forms.CharField(label=_("Fax"))
    billing = forms.MultipleChoiceField(
        label=_("BillingDetails"),
        choices=Billing_Details,
        widget=forms.CheckboxSelectMultiple(),
    )
    newsletter = forms.CharField(widget=forms.CheckboxInput(), label=_("Newsletter"))
