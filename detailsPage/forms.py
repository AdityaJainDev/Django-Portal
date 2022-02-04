from django import forms
from localflavor.generic.forms import BICFormField, IBANFormField 

PAYMENT_CHOICES =(
    ("1", "Zahlung per Überweisung"),
    ("0", "Zahlung per Lastschrift"),
)

class PaymentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['account_number'].disabled = True

    account_number = forms.CharField(max_length = 100)
    options = forms.ChoiceField(choices = PAYMENT_CHOICES)
    owner = forms.CharField(max_length = 100)
    iban = IBANFormField()
    bic = BICFormField()
    
    class Meta:
        exclude =('sort_code', 'bank',)
        