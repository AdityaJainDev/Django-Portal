from django.urls import path
from . import views
from .views import password_reset, change_password, edit_personal_data

app_name = "dashboard"

urlpatterns = [
    path("main/", views.index, name="main"),
    path(
        "invoice_details/<int:rechnung_id>",
        views.invoice_details,
        name="invoice_details",
    ),
    path("all_invoices/", views.all_invoices, name="all_invoices"),
    path("edit_personal_data/", edit_personal_data.as_view(), name="edit_personal_data"),
    path("password_reset/", password_reset.as_view(), name="password_reset"),
    path("change_password/", change_password.as_view(), name="change_password"),
    path(
        "download_pdf/<int:rechnung_rnr>/<int:rechnung_id>",
        views.download_pdf,
        name="download_pdf",
    ),
    path("logout/", views.logout, name="logout"),
]
