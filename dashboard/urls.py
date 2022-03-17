from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('main/', views.index, name='main'),
    path('invoice_details/', views.invoice_details, name='invoice_details'),
    path('edit_personal_data/', views.edit_personal_data, name='edit_personal_data'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('change_password/', views.change_password, name='change_password'),
]
