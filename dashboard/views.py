from multiprocessing import context
from sre_constants import SUCCESS
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from .forms import PasswordResetForm, ChangePassword, PersonalDataEdit
from django.conf import settings
import requests
from django.utils.translation import gettext as _
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import mimetypes
from django.contrib.auth.models import User
import os
# Create your views here.


home_link = 'dashboard:home'

@require_GET
@login_required
def home(request):
    return render(request, "registration/login.html")


@require_GET
def logout(request):
    u = User.objects.get(username=request.user.username)
    u.delete()
    request.session.clear()
    return HttpResponseRedirect('accounts/login/')

@require_GET
@login_required
def index(request):
    try:
        if request.user.last_login.replace(microsecond=0) == request.user.date_joined.replace(microsecond=0):
            return HttpResponseRedirect(reverse('dashboard:change_password'))
        else:
            account_number = request.session['username']
            password = request.session['password']

            invoice = requests.get(
                settings.CRM_ENDPOINT + "Rechnungen/Rechnungen/", auth=(account_number, password))
            personal = requests.get(
                settings.CRM_ENDPOINT + "Kunden/Kunde/", auth=(account_number, password))

            if invoice.json()["status"] == 1 and personal.json()["status"] == 1:
                invoices = invoice.json()["data"]
                personal_data = personal.json()["data"]
                context = {"values": invoices, "personal": personal_data}
            return render(request, "home_main.html", context)
    except Exception as e:
        print(e)
    return render(request, "home_main.html")

@require_GET
@login_required
def invoice_details(request, rechnung_id):
    account_number = request.session['username']
    password = request.session['password']
    invoice_id = rechnung_id

    params = {"rechnung_id": invoice_id}

    invoice_detail = requests.get(settings.CRM_ENDPOINT + "Rechnungen/RechnungDetails/", auth=(account_number, password), params=params)
    list_items = requests.get(settings.CRM_ENDPOINT + "Rechnungen/RechnungPositionen/", auth=(account_number, password), params=params)

    if invoice_detail.json()["status"] == 1:
        invoices = invoice_detail.json()["data"]
        list_items = list_items.json()["data"]
        context = {"values": invoices, "list_items": list_items}
    return render(request, "invoices.html", context)

@require_GET
@login_required
def all_invoices(request):
    account_number = request.session['username']
    password = request.session['password']

    invoice = requests.get(settings.CRM_ENDPOINT + "Rechnungen/Rechnungen/", auth=(account_number, password))

    if invoice.json()["status"] == 1:
        invoices = invoice.json()["data"]
        context = {"values": invoices}
    return render(request, "all_invoices.html", context)


@require_GET
@login_required
def edit_personal_data(request):
    if request.method == 'GET':
        form = PersonalDataEdit()
    elif request.method == 'POST':
        form = PersonalDataEdit(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            postcode = form.cleaned_data['postcode']
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            fax = form.cleaned_data['fax']
            billing = form.cleaned_data['billing']
            newsletter = form.cleaned_data['newsletter']

            account_number = request.session['username']
            password = request.session['password']


            data = {"kunde_firma": company, "kunde_vorname": first_name, "kunde_name": last_name, "kunde_adresse": address,
                    "kunde_plz": postcode, "kunde_ort": city, "kunde_land": country, "kunde_email": email, "kunde_telefon": phone,
                    "kunde_telefax": fax, "kunde_sendmail": billing, "kunde_newsletter_marketing": newsletter}

            edit_data = requests.post(settings.CRM_ENDPOINT + "Kunden/StammdatenEdit/", auth=(account_number, password), data=data)

            if edit_data.json()["status"] == 1:
                messages.success(request, _('EditDataSuccess'))
                return HttpResponseRedirect(reverse(home_link))
            else:
                messages.error(request, _('EditDataError'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'form': form})

    context = {'form': form}

    return render(request, "edit_data.html", context)


@require_GET
def password_reset(request):
    if request.method == 'GET':
        form = PasswordResetForm()

    elif request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            account_number = request.user.username

            data = {'knr': account_number, "email": email}

            data = requests.post(settings.CRM_ENDPOINT +
                                 "Kunden/LostPW/", data)

            if data.json()["status"] == 1:
                messages.success(request, _('ResetEmailSuccess'))
                return HttpResponseRedirect(reverse(home_link))
            else:
                messages.error(request, _('ResetEmailError'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'form': form})

    context = {'form': form}

    return render(request, "registration/reset_password.html", context)

@require_GET
@login_required
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
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'form': form})
            elif request.user.check_password(password) is SUCCESS:
                messages.error(request, _('OldPasswordError'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'form': form})
            else:
                data = {'knr': request.user.username, "alt_pwd": password,
                        "neu_pwd": new_password, "neu_verify_pwd": confirm_password}
                send_request = requests.post(settings.CRM_ENDPOINT + "Kunden/ChangePWD/", auth=(
                    request.session['username'], request.session['password']), data=data)

                if send_request.json()["status"] == 1:
                    request.session['password'] = new_password
                    messages.success(request, _('PasswordChangeSuccess'))
                    return HttpResponseRedirect(reverse(home_link))
                else:
                    messages.error(request, _('PasswordChangeError'))
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'form': form})

    context = {'form': form}

    return render(request, "registration/reset_password.html", context)