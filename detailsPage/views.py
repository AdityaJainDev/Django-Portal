from django.shortcuts import render
from .forms import PaymentForm
from django.http import HttpResponse, HttpResponseRedirect
import requests
from urllib import parse
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "base.html")


def sepa_payment(request):

    if request.method == 'GET':
        form = PaymentForm()
        form.initial['account_number'] = request.GET.get('knr', None)
        form.initial['options'] = "1"

    elif request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            account_number = request.GET.get('knr', None)
            owner = form.cleaned_data['owner']
            iban = form.cleaned_data['iban']
            bic = form.cleaned_data['bic']
            options = form.cleaned_data['options']
            token = request.GET.get('token', None)
            
            data = {"inhaber": owner, "iban": iban, "bic": bic, 'knr':account_number, 'token':token, 'zahlungsart':options}

            crm_endpoint = "https://ascrm.aditsystems.de/api/Kunden/SEPA"

            save_data = requests.post(crm_endpoint, data)
            
            if save_data.json()['status'] == -1:
                messages.success(request, save_data.json()['msg'])
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.success(request, 'Data updated successfully')
                return HttpResponseRedirect("/")

    context = {'form':form}

    return render(request, "form.html", context)