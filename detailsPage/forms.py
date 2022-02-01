from django import forms
from localflavor.generic.forms import BICFormField, IBANFormField 



class PaymentForm(forms.Form):
 
    owner = forms.CharField(max_length = 100)
    account_number = forms.CharField(max_length = 100)
    sort_code = forms.CharField(max_length = 100)
    iban = IBANFormField()
    bic = BICFormField()
    bank = forms.CharField(max_length=100)