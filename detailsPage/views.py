from django.shortcuts import render
from .forms import PaymentForm
from django.http import HttpResponse
import requests
from urllib import parse

# Create your views here.
def index(request):
    return render(request, "base.html")


def sepa_payment(request):

    url = "https://ascrm.aditsystems.de/api/Kunden/SEPA/?knr=12072&token=Ncj7H6xDeyJm"

    knr=parse.parse_qs(parse.urlparse(url).query)['knr'][0]
    token=parse.parse_qs(parse.urlparse(url).query)['token'][0]

    info = requests.get(url)

    if request.method == 'GET':
        form = PaymentForm()
        form.initial['account_number'] = "K" + knr
        form.initial['options'] = '2'

    elif request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.cleaned_data['account_number'] = knr
            owner = form.cleaned_data['owner']
            iban = form.cleaned_data['iban']
            bic = form.cleaned_data['bic']
            options = form.cleaned_data['options']

            print(options)
            
            data = {"inhaber": owner, "iban": iban, "bic":bic, 'knr':knr, 'token':token, 'zahlungsart':options }

            x = requests.post(url, data)

            if x.json()['status'] == -1:
                return HttpResponse(x.json()['msg'])
            else:
                return HttpResponse('Details updated succesfully.')

    context = {'form':form,}

    return render(request, "form.html", context)