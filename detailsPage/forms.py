from django import forms
from localflavor.generic.forms import BICFormField, IBANFormField 

PAYMENT_CHOICES =(
    ("0", "Zahlung per Überweisung"),
    ("1", "Zahlung per Lastschrift"),
)

class PaymentForm(forms.Form):
    account_number = forms.CharField(max_length = 100, required = False)
    options = forms.ChoiceField(choices = PAYMENT_CHOICES)
    owner = forms.CharField(max_length = 100, required = False)
    iban = IBANFormField(required = False)
    bic = BICFormField(required = False)

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['account_number'].disabled = True
        