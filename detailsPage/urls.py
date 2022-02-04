from django.urls import path, re_path
from .views import index
from . import views

app_name = 'detailsPage'

urlpatterns = [
    path('', views.index, name='home'),
    re_path(r'^payment/(?:knr=(?P<knr>\d+)&:token(?P<token>\d+))?$', views.sepa_payment, name='payment')
]
