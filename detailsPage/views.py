from django.shortcuts import render
from .forms import PaymentForm
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "base.html")


def sepa_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Your review has been taken')
    else:
        form = PaymentForm()
        context = {'form':form}   
    
    return render(request, "form.html", context)