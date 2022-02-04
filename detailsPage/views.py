from django.shortcuts import render
from .forms import PaymentForm
from django.http import HttpResponse
import requests
from urllib import parse

# Create your views here.
def index(request):
    return render(request, "base.html")


def sepa_payment(request):

    if request.method == 'GET':
        form = PaymentForm()
        form.initial['account_number'] = request.GET.get('knr', None)


    elif request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.cleaned_data['account_number'] = request.GET.get('knr', None)
            owner = form.cleaned_data['owner']
            iban = form.cleaned_data['iban']
            bic = form.cleaned_data['bic']
            options = form.cleaned_data['options']
            
            data = {"inhaber": owner, "iban": iban, "bic":bic, 'knr':request.GET.get('knr', None), 'token':request.GET.get('token', None), 'zahlungsart':options }

            #Still need to configure this part
            knr = request.POST['knr']

            if x.json()['status'] == -1:
                return HttpResponse(x.json()['msg'])
            else:
                return HttpResponse('Details updated succesfully.')

    context = {'form':form}

    return render(request, "form.html", context)