from django import forms
from django.forms import formset_factory
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


DOMAIN_DELETION = (
    ("0", _("EndOfTerm")),
    ("1", _("ChangeProvider")),
    ("2", _("Custom")),
)

DOMAIN_HANDLING = (
    ("0", _("Delete")),
    ("1", _("SendAuth")),
)

class CancellationForm(forms.Form):
    name =  forms.CharField(label=_("CancelName"), max_length=100, required=True)
    customer_number = forms.IntegerField(label=_("CancelNumber"), required=True)
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'style': 'width:50%', 'type':'number'}))
    contract_number = forms.CharField(label=_("CancelContract"), max_length=100, required=True)
    email = forms.EmailField(label=_("CancelEmail"), max_length=100, required=True)
    confirm_tariff = forms.BooleanField(label=_("CancelTariff"), required=True)
    confirm_consumer = forms.BooleanField(label=_("CancelConsumer"), required=True)
    domain_options = forms.ChoiceField(label=_("CancelOptions"), required=True, choices=DOMAIN_DELETION)
    additional_data = forms.CharField(label=_("AdditionalData"), required=False, widget=forms.Textarea)
    confirm_data = forms.BooleanField(label=_("CancelData"), required=True)
    confirm_data_deletion = forms.BooleanField(label=_("CancelDeletion"), required=True)
    field_garb = forms.BooleanField(required=False)

# Make a django formset_factory class

class DomainForm(forms.Form):
    domain_name = forms.CharField(required=False)
    domain_handling = forms.ChoiceField(choices=DOMAIN_HANDLING, required=False)

DomainFormset = formset_factory(DomainForm)