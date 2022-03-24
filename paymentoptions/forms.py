from django import forms
from localflavor.generic.forms import BICFormField, IBANFormField
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import Widget, CheckboxInput, boolean_check

PAYMENT_CHOICES = (
    ("0", _("Bank Transfer")),
    ("1", _("Direct Debit")),
)


class PaymentForm(forms.Form):
    account_number = forms.CharField(
        label=_("AccountNumber"), max_length=100, required=False
    )
    payment_options = forms.MultipleChoiceField(
        label=_("options"),
        choices=PAYMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
    )
    owner = forms.CharField(label=_("owner"), max_length=100, required=False)
    iban = IBANFormField(label=_("iban"), required=False)
    bic = BICFormField(label=_("bic"), required=False)
    confirm = forms.BooleanField(label=_("Accept"), required=False)

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['account_number'].disabled = True