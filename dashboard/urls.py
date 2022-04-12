from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('main/', views.index, name='main'),
    path('invoice_details/<int:rechnung_id>', views.invoice_details, name='invoice_details'),
    path('all_invoices/', views.all_invoices, name='all_invoices'),
    path('edit_personal_data/', views.edit_personal_data, name='edit_personal_data'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('change_password/', views.change_password, name='change_password'),
    path('download_pdf/<str:rechnung_rnr>/<str:rechnung_id>', views.download_pdf, name='download_pdf'),
]
