from django import forms
from localflavor.generic.forms import BICFormField, IBANFormField 
from django.utils.translation import gettext_lazy as _

PAYMENT_CHOICES =(
    ("0", _("Bank Transfer")),
    ("1", _("Direct Debit")),
)

class PaymentForm(forms.Form):
    account_number = forms.CharField(label=_('AccountNumber'), max_length = 100, required = False)
    options = forms.ChoiceField(label=_('options'), choices = PAYMENT_CHOICES)
    owner = forms.CharField(label=_('owner'), max_length = 100, required = False)
    iban = IBANFormField(label= "IBAN", required = False)
    bic = BICFormField(label= "BIC", required = False)

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['account_number'].disabled = True
        