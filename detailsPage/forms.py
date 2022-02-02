from django import forms
from .models import SepaModel
from localflavor.generic.forms import BICFormField, IBANFormField 

class PaymentForm(forms.ModelForm):
    iban = IBANFormField()
    bic = BICFormField()
    class Meta:
        model = SepaModel
        fields =('owner','account_number','sort_code', 'bank',)
        