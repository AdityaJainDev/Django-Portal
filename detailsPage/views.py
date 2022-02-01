from django.shortcuts import render
from .forms import PaymentForm

# Create your views here.
def index(request):
    context ={}
    context['form']= PaymentForm()
    return render(request, "base.html", context)