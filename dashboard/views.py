from multiprocessing import context
from sre_constants import SUCCESS
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from .forms import PasswordResetForm, ChangePassword
from django.conf import settings
import requests
from django.utils.translation import gettext as _
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.contrib.auth.models import User
# Create your views here.


@require_GET
def home(request):
    return render(request, "home.html")

@require_GET
def logout(request):
    u = User.objects.get(username = request.user.username)
    u.delete()
    request.session.clear()
    return HttpResponseRedirect('/login/')


@require_GET
def index(request):
    try:
        if request.user.last_login.replace(microsecond=0) == request.user.date_joined.replace(microsecond=0):
            return HttpResponseRedirect(reverse('dashboard:change_password'))
        else:
            account_number = request.session['username']
            password = request.session['password']

            invoice = requests.get(settings.CRM_ENDPOINT + "Rechnungen/Rechnungen/", auth=(account_number, password))
            personal = requests.get(settings.CRM_ENDPOINT + "Kunden/Kunde/", auth=(account_number, password))

            if invoice.json()["status"] == 1 and personal.json()["status"] == 1:
                invoices = invoice.json()["data"]
                personal_data = personal.json()["data"]
                context = {"values": invoices, "personal": personal_data}
            return render(request, "dashboard/home.html", context)
    except Exception as e:
        print(e)
    return render(request, "dashboard/home.html")


@require_GET
def invoice_details(request):
    account_number = request.session['username']
    password = request.session['password']

    invoice = requests.get(settings.CRM_ENDPOINT + "Rechnungen/Rechnungen/", auth=(account_number, password))
    invoice_detail = requests.get(settings.CRM_ENDPOINT + "Rechnungen/RechnungDetails/", auth=(account_number, password), params={"rechnung_id": "34415"})

    if invoice_detail.json()["status"] == 1:
        invoices = invoice.json()["data"]
        context = {"values": invoices}
    return render(request, "dashboard/invoices.html", context)


@require_POST
def password_reset(request):
    if request.method == 'GET':
        form = PasswordResetForm()

    elif request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            account_number = request.user.username

            data = {'knr':account_number, "email": email}

            data = requests.post(settings.CRM_ENDPOINT + "Kunden/LostPW/", data)

            if data.json()["status"] == 1:
                messages.success(request, _('ResetEmailSuccess'))
                return HttpResponseRedirect(reverse('dashboard:home'))
            else:
                messages.error(request, _('ResetEmailError'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'form':form})
    
    context = {'form':form}

    return render(request, "registration/reset_password.html", context)

@require_POST
def change_password(request):
    if request.method == 'GET':
        form = ChangePassword()

    elif request.method == 'POST':
        form = ChangePassword(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if new_password != confirm_password:
                messages.error(request, _('PasswordMatchError'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'form':form})
            elif request.user.check_password(password) is SUCCESS:
                messages.error(request, _('OldPasswordError'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'form':form})
            else:
                data = {'knr':request.user.username, "alt_pwd": password, "neu_pwd":new_password, "neu_verify_pwd":confirm_password}
                send_request = requests.post(settings.CRM_ENDPOINT + "Kunden/ChangePWD/", auth=(request.session['username'], request.session['password']), data=data)

                if send_request.json()["status"] == 1:
                    request.session['password'] = new_password
                    messages.success(request, _('PasswordChangeSuccess'))
                    return HttpResponseRedirect(reverse('dashboard:home'))
                else:
                    messages.error(request, _('PasswordChangeError'))
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'form':form})
    
    context = {'form':form}

    return render(request, "registration/reset_password.html", context)