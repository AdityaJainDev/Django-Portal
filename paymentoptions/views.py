import logging
from django.shortcuts import render, redirect
from .forms import PaymentForm
import requests
from django.utils.translation import gettext as _
from django.contrib import messages
from django.conf import settings
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)

form_template = "form.html"

# Create your views here.
class paymentoptions(TemplateView):
    def get(self, request, *args, **kwargs):
        customer_number = request.GET.get("knr", None)
        token = request.GET.get("token", None)
        data = {"knr": customer_number, "token": token}

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
            form.initial["customer_number"] = customer_number
            form.initial["payment_options"] = zahlungsart

        context = {"form": form, "customer_number": customer_number}

        return render(request, form_template, context)

    def post(self, request, *args, **kwargs):
        form = PaymentForm(request.POST)
        customer_number = request.GET.get("knr", None)
        if form.is_valid():
            customer_number = form.cleaned_data["customer_number"]
            owner = form.cleaned_data["owner"]
            iban = form.cleaned_data["iban"]
            bic = form.cleaned_data["bic"]
            options = form.cleaned_data["payment_options"]
            token = request.GET.get("token", None)

            data = {
                "inhaber": owner,
                "knr": customer_number,
                "token": token,
                "zahlungsart": options,
            }

            if iban:
                data = {
                    "inhaber": owner,
                    "iban": iban,
                    "bic": bic,
                    "knr": customer_number,
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
                form.initial["customer_number"] = request.GET.get("knr", None)
                form.initial["payment_options"] = "1"
            else:
                if iban:
                    messages.success(request, _("DD Success Message"))
                else:
                    messages.success(request, _("BT Success Message"))
        else:
            for issue in form.errors:
                messages.error(request, form.errors[issue])
            
        return render(request, form_template, {"form": form,"customer_number": customer_number})

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