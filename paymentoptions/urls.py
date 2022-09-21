from django.urls import path
from .views import paymentoptions
from django.views.generic import TemplateView

app_name = "paymentoptions"

urlpatterns = [
    path("", paymentoptions.as_view(), name="payment"),
    path("error", TemplateView.as_view(template_name="token_error.html"), name="token_error"),
]
