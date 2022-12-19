from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

DOMAIN_DELETION = (
    ("0", _("EndOfTerm")),
    ("1", _("ChangeProvider")),
)

class CancellationForm(forms.Form):
    name =  forms.CharField(label=_("CancelName"), max_length=100, required=True)
    customer_number = forms.CharField(label=_("CancelNumber"), max_length=100, required=True)
    phone_number = forms.IntegerField(label=_("CancelPhoneNumber"), required=True)
    contract_number = forms.CharField(label=_("CancelContract"), max_length=100, required=True)
    email = forms.EmailField(label=_("CancelEmail"), max_length=100, required=True)
    confirm_tariff = forms.BooleanField(label=_("CancelTariff"), required=False)
    confirm_consumer = forms.BooleanField(label=_("CancelConsumer"), required=False)
    domain_options = forms.ChoiceField(label=_("CancelOptions"), choices=DOMAIN_DELETION)
    additional_data = forms.CharField(label=_("AdditionalData"), required=False, widget=forms.Textarea)
    confirm_data = forms.BooleanField(label=_("CancelData"), required=False)
    confirm_data_deletion = forms.BooleanField(label=_("CancelDeletion"), required=False)
    field_garb = forms.BooleanField(required=False)
