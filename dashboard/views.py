import logging
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from .forms import PasswordResetForm, ChangePassword, PersonalDataEdit
from django.conf import settings
import requests
from django.utils.translation import gettext as _
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import base64
from django.contrib.auth import logout as auth_logout
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied

try:
    from .models import APIData
except Exception as e:
    pass

# Create your views here.


home_link = "dashboard:main"
logger = logging.getLogger(__name__)
password_reset_template = "registration/reset_password.html"
change_password_template = "registration/change_password.html"


@require_GET
def logout(request):
    try:
        user = User.objects.get(username=request.user.username)
        data = APIData.objects.get(account_number=request.user.username)
        user.delete()
        data.delete()
    except Exception as exec:
        logger.error(exec)
        request.session.clear()
        auth_logout(request)
    return HttpResponseRedirect("/accounts/login/")


@require_GET
@login_required
def index(request):
    try:
        data=APIData.objects.get(account_number=request.user.username)
        account_number = data.account_number
        password = data.password

        print(data.account_number, data.password)

        try:
            invoice = requests.get(
                settings.CRM_ENDPOINT + "Rechnungen/Rechnungen/",
                auth=(account_number, password),
            )
            personal = requests.get(
                settings.CRM_ENDPOINT + "Kunden/Kunde/",
                auth=(account_number, password),
            )
            invoice.raise_for_status()
        except Exception as exec:
            logger.error(exec)
            raise PermissionDenied()

        if invoice.json()["status"] == 1 and personal.json()["status"] == 1:
            invoices = invoice.json()["data"]
            personal_data = personal.json()["data"]
            context = {"values": invoices, "personal": personal_data}
        return render(request, "home_main.html", context)
    except Exception as exec:
            logger.debug(exec)
    return render(request, "home_main.html")


@require_GET
@login_required
def invoice_details(request, rechnung_id):
    data=APIData.objects.get(account_number=request.user.username)
    account_number = data.account_number
    password = data.password
    invoice_id = rechnung_id

    params = {"rechnung_id": invoice_id}

    try:
        invoice_detail = requests.get(
            settings.CRM_ENDPOINT + "Rechnungen/RechnungDetails/",
            auth=(account_number, password),
            params=params,
        )
        list_items = requests.get(
            settings.CRM_ENDPOINT + "Rechnungen/RechnungPositionen/",
            auth=(account_number, password),
            params=params,
        )
        invoice_detail.raise_for_status()
    except Exception as exec:
        logger.error(exec)
        raise PermissionDenied()
        

    if invoice_detail.json()["status"] == 1:
        invoices = invoice_detail.json()["data"]
        list_items = list_items.json()["data"]
        context = {"values": invoices, "list_items": list_items}
    return render(request, "invoices.html", context)


@require_GET
@login_required
def all_invoices(request):
    data=APIData.objects.get(account_number=request.user.username)
    account_number = data.account_number
    password = data.password

    try:
        invoice = requests.get(
            settings.CRM_ENDPOINT + "Rechnungen/Rechnungen/",
            auth=(account_number, password),
        )
        invoice.raise_for_status()
    except Exception as exec:
        logger.error(exec)
        raise PermissionDenied()

    if invoice.json()["status"] == 1:
        invoices = invoice.json()["data"]
        context = {"values": invoices}
    return render(request, "all_invoices.html", context)


class edit_personal_data(TemplateView):
    def get(self, request, *args, **kwargs):
        form = PersonalDataEdit()
        context = {"form": form}
        return render(request, "edit_data.html", context)

    def post(self, request, *args, **kwargs):
        form = PersonalDataEdit(request.POST)
        if form.is_valid():
            company = form.cleaned_data["company"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            address = form.cleaned_data["address"]
            postcode = form.cleaned_data["postcode"]
            city = form.cleaned_data["city"]
            country = form.cleaned_data["country"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            fax = form.cleaned_data["fax"]
            billing = form.cleaned_data["billing"]
            newsletter = form.cleaned_data["newsletter"]

            data=APIData.objects.get(account_number=request.user.username)
            account_number = data.account_number
            password = data.password

            data = {
                "kunde_firma": company,
                "kunde_vorname": first_name,
                "kunde_name": last_name,
                "kunde_adresse": address,
                "kunde_plz": postcode,
                "kunde_ort": city,
                "kunde_land": country,
                "kunde_email": email,
                "kunde_telefon": phone,
                "kunde_telefax": fax,
                "kunde_sendmail": billing,
                "kunde_newsletter_marketing": newsletter,
            }

            try:
                edit_data = requests.post(
                    settings.CRM_ENDPOINT + "Kunden/StammdatenEdit/",
                    auth=(account_number, password),
                    data=data,
                )
                edit_data.raise_for_status()
            except Exception as exec:
                logger.error(exec)
                raise PermissionDenied()

            if edit_data.json()["status"] == 1:
                messages.success(request, _("EditDataSuccess"))
                return HttpResponseRedirect(reverse(home_link))
            else:
                messages.error(request, _("EditDataError"))
                return HttpResponseRedirect(
                    request.META.get("HTTP_REFERER"), {"form": form}
                )

        context = {"form": form}

        return render(request, "edit_data.html", context)


class password_reset(TemplateView):
    def get(self, request, *args, **kwargs):
        form = PasswordResetForm()
        context = {"form": form}
        return render(request, password_reset_template, context)
    
    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            data=APIData.objects.get(account_number=request.user.username)
            account_number = data.account_number

            data = {"knr": account_number, "email": email}

            try:
                data = requests.post(settings.CRM_ENDPOINT + "Kunden/LostPW/", data)
                data.raise_for_status()
            except Exception as exec:
                logger.error(exec)
                raise PermissionDenied()

            if data.json()["status"] == 1:
                messages.success(request, _("ResetEmailSuccess"))
                return HttpResponseRedirect(reverse(home_link))
            else:
                messages.error(request, _("ResetEmailError"))
                return HttpResponseRedirect(
                    request.META.get("HTTP_REFERER"), {"form": form}
                )

        context = {"form": form}

        return render(request, password_reset_template, context)


class change_password(TemplateView):
    def get(self, request, *args, **kwargs):
        form = ChangePassword()
        context = {"form": form}
        return render(request, change_password_template, context)
    
    def post(self, request, *args, **kwargs):
        form = ChangePassword(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            new_password = form.cleaned_data["new_password"]
            confirm_password = form.cleaned_data["confirm_password"]

            if new_password != confirm_password:
                messages.error(request, _("PasswordMatchError"))
                return HttpResponseRedirect(
                    request.META.get("HTTP_REFERER"), {"form": form}
                )
            elif request.user.check_password(password) == True:
                messages.error(request, _("OldPasswordError"))
                return HttpResponseRedirect(
                    request.META.get("HTTP_REFERER"), {"form": form}
                )
            else:
                data = {
                    "knr": request.user.username,
                    "alt_pwd": password,
                    "neu_pwd": new_password,
                    "neu_verify_pwd": confirm_password,
                }

                try:
                    send_request = requests.post(
                        settings.CRM_ENDPOINT + "Kunden/ChangePWD/",
                        auth=(request.session["username"], request.session["password"]),
                        data=data,
                    )
                    send_request.raise_for_status()
                except Exception as exec:
                    logger.error(exec)

                if send_request.json()["status"] == 1:
                    request.session["password"] = new_password
                    messages.success(request, _("PasswordChangeSuccess"))
                    return HttpResponseRedirect(reverse(home_link))
                else:
                    messages.error(request, _("PasswordChangeError"))
                    return HttpResponseRedirect(
                        request.META.get("HTTP_REFERER"), {"form": form}
                    )

        context = {"form": form}

        return render(request, change_password_template, context)


@require_GET
@login_required
def download_pdf(request, rechnung_rnr, rechnung_id):
    data=APIData.objects.get(account_number=request.user.username)
    account_number = data.account_number
    password = data.password
    rnr = rechnung_rnr

    params = {"rechnung_id": rechnung_id}

    try:
        download_pdf = requests.get(
            settings.CRM_ENDPOINT + "Rechnungen/RechnungPDF/",
            auth=(account_number, password),
            params=params,
        )
        invoice_detail = requests.get(
            settings.CRM_ENDPOINT + "Rechnungen/RechnungDetails/",
            auth=(account_number, password),
            params=params,
        )
        download_pdf.raise_for_status()
        invoice_detail.raise_for_status()

    except Exception as exec:
        logger.error(exec)
        raise PermissionDenied()

    values = invoice_detail.json()["data"]

    if values["rechnung_rnr"] == str(rnr) and download_pdf.json()["status"] == 1:
        jsondata = download_pdf.json()["data"]
        decoded = base64.b64decode(jsondata)
        response = HttpResponse(decoded, content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="RE{}.pdf"'.format(rnr)
        return response


def error_404(request, exception, template_name="errors/404.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response

def error_403(request, exception, template_name="errors/403.html"):
    response = render(request, template_name)
    response.status_code = 403
    return response

def error_400(request, exception, template_name="errors/400.html"):
    response = render(request, template_name)
    response.status_code = 400
    return response

def error_500(request, template_name="errors/500.html"):
    response = render(request, template_name)
    response.status_code = 500
    return response