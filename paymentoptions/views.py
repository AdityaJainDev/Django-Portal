import logging
from django.shortcuts import render, redirect
from .forms import PaymentForm
from django.http import HttpResponse, HttpResponseRedirect
import requests
from django.utils.translation import gettext as _
from django.contrib import messages
from django.conf import settings
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)

# Create your views here.
class paymentoptions(TemplateView):
    def get(self, request, *args, **kwargs):
        account_number = request.GET.get("knr", None)
        token = request.GET.get("token", None)
        data = {"knr": account_number, "token": token}

        try:
            save_data = requests.get(
                settings.CRM_ENDPOINT + "Kunden/SEPA/", params=data
            )
            save_data.raise_for_status()
        except Exception as exec:
            logger.error(exec)

        if save_data.json()["status"] == -1:
            return redirect("paymentoptions:token_error")
        else:
            zahlungsart = save_data.json()["zahlungsart"]
            form = PaymentForm()
            form.initial["account_number"] = request.GET.get("knr", None)
            form.initial["payment_options"] = zahlungsart

        context = {"form": form}

        return render(request, "form.html", context)

    def post(self, request, *args, **kwargs):
        form = PaymentForm(request.POST)
        if form.is_valid():
            account_number = request.GET.get("knr", None)
            owner = form.cleaned_data["owner"]
            iban = form.cleaned_data["iban"]
            bic = form.cleaned_data["bic"]
            options = form.cleaned_data["payment_options"]
            token = request.GET.get("token", None)

            if iban == "":
                data = {
                    "inhaber": owner,
                    "knr": account_number,
                    "token": token,
                    "zahlungsart": options,
                }
            
            else:
                data = {
                    "inhaber": owner,
                    "iban": iban,
                    "bic": bic,
                    "knr": account_number,
                    "token": token,
                    "zahlungsart": options,
                }

            try:
                save_data = requests.post(settings.CRM_ENDPOINT + "Kunden/SEPA/", data=data)
                save_data.raise_for_status()
            except Exception as exec:
                logger.error(exec)

            if save_data.json()["status"] == -1:
                messages.error(request, _("Error Message"))
                form = PaymentForm()
                form.initial["account_number"] = request.GET.get("knr", None)
                form.initial["payment_options"] = "1"
                return HttpResponseRedirect(
                    request.META.get("HTTP_REFERER"), {"form": form}
                )
            else:
                return redirect("paymentoptions:success")
        else:
            print(form.errors.keys)
            for issue in form.errors:
                messages.error(request, form.errors[issue])
            form = PaymentForm()
            form.initial["account_number"] = request.GET.get("knr", None)
            form.initial["payment_options"] = "1"


        context = {"form": form}

        return render(request, "form.html", context)


def error_404(request, exception):
    return render(request, "errors/404.html", {})


def error_500(request, exception=None):
    return render(request, "errors/500.html", {})


def error_403(request, exception=None):
    return render(request, "errors/403.html", {})


def error_400(request, exception=None):
    return render(request, "errors/400.html", {})
