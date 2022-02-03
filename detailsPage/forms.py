from django import forms
from .models import SepaModel
from localflavor.generic.forms import BICFormField, IBANFormField 

PAYMENT_CHOICES =(
    ("1", "Zahlung per Überweisung"),
    ("0", "Zahlung per Lastschrift"),
)

class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['account_number'].disabled = True

    iban = IBANFormField()
    bic = BICFormField()
    options = forms.ChoiceField(choices = PAYMENT_CHOICES)
    class Meta:
        model = SepaModel
        fields =('account_number', 'options', 'owner',)
        