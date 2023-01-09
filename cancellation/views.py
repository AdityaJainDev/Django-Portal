from django.shortcuts import render
from .forms import CancellationForm, DomainFormset
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib import messages
import logging

form_template2 = "cancellation_form.html"
email_text = "mail_cancellation.txt"
email_template = "mail_cancellation.html"
support_email = "mail_cancellation_support.html"
support_text = "mail_cancellation_support.txt"

logger = logging.getLogger(__name__)

def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Create your views here.
class cancellation(TemplateView):
    def get(self, request, *args, **kwargs):
        form = CancellationForm()
        formset = DomainFormset()

        dict_1 = {'Test1': "Delete", "test2": "send"}
        context = {"form": form, "domain_formset": formset, "dict_1": dict_1}
        return render(request, form_template2, context)
    
    def post(self, request, *args, **kwargs):
        form = CancellationForm(request.POST)
        formset = DomainFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            name = form.cleaned_data["name"]
            customer_number = form.cleaned_data["customer_number"]
            phone_number = form.cleaned_data["phone_number"]
            contract_number = form.cleaned_data["contract_number"]
            email = form.cleaned_data["email"]
            domain_options = form.cleaned_data["domain_options"]
            additional_data = form.cleaned_data["additional_data"]
            honeypot = form.cleaned_data["field_garb"]
            user_ip = request.META.get('REMOTE_ADDR')
            user_browser = request.META['HTTP_USER_AGENT']

            domain_dict = {}
            for link_form in formset:
                domain_name = link_form.cleaned_data["domain_name"]
                domain_handling = link_form.cleaned_data["domain_handling"]
                if domain_handling == str(0):
                    domain_handling = _("Delete")
                else:
                    domain_handling = _("SendAuth")
                domain_dict[domain_name] = domain_handling

            if honeypot:
                messages.error(request, _("SpamMessage"))
                logger.error(ValidationError(_("Spam")))
                raise ValidationError(_("Spam"))

            if domain_options == str(0):
                domain = _("DomainDeletion")
            elif domain_options == str(1):
                domain = _("DomainTransfer")
            else:
                domain = _("CustomSelection")

            now = datetime.now()
            
            replacements = {
            "value": now,
            "name": name,
            "customer_number": customer_number,
            "phone_number" : phone_number,
            "contract_number": contract_number,
            "domain_options": domain,
            "additional_data": additional_data,
            "domain_dict": domain_dict,
            "email": email,
            }

            replacements_support = {
            "value": now,
            "name": name,
            "customer_number": customer_number,
            "phone_number" : phone_number,
            "contract_number": contract_number,
            "domain_options": domain,
            "domain_dict": domain_dict,
            "additional_data": additional_data,
            "email": email,
            "user_ip": user_ip,
            "user_browser": user_browser,
            }

            body = render_to_string(email_text, replacements)
            body_html = render_to_string(email_template, replacements)
            body_support = render_to_string(support_text, replacements_support)
            body_html_support = render_to_string(support_email, replacements_support)
            
            msg = EmailMultiAlternatives(_("CancelSubject"), body, settings.EMAIL_FROM, [email])
            msg.attach_alternative(body_html, "text/html")
            msg.send()

            msg1 = EmailMultiAlternatives(_("SupportSubject"), body_support, settings.EMAIL_FROM, [settings.EMAIL_SUPPORT])
            msg1.attach_alternative(body_html_support, "text/html")
            msg1.send()

            messages.success(request, _("CustomerFormSuccess"))
        else:
            messages.error(request, _("CustomerFormError"))
            
        return render(request, form_template2, {"form": form, "formset": formset})