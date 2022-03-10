from django.shortcuts import render
from django.views.decorators.http import require_GET
from .forms import PasswordResetForm
from django.conf import settings
import requests
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

@require_GET
def index(request):
    return render(request, "home.html")


def password_reset(request):
    if request.method == 'GET':
        form = PasswordResetForm()

    elif request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            account_number = request.GET.get('knr', None)

            data = {'knr':account_number, "email": email}

            data = requests.post(settings.CRM_ENDPOINT + "LostPW/", data)

            if data.json()["status"] == 1:
                messages.success(request, "Password reset email sent successfully.")
                return HttpResponseRedirect(reverse('dashboard:home'))
            else:
                messages.error(request, "Something went wrong, please try again.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'form':form})
    
    context = {'form':form}

    return render(request, "registration/reset_password.html", context)