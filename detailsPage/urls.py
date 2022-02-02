from django.urls import path
from .views import index
from . import views

app_name = 'detailsPage'

urlpatterns = [
    path('', views.index, name='home'),
    path('payment', views.sepa_payment, name='payment'),
]
