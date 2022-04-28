from django.urls import path, re_path
from .views import paymentoptions

app_name = 'paymentoptions'

urlpatterns = [
    path('details', paymentoptions.as_view(), name='payment'),
]
