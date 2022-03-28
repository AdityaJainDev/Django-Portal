from django.urls import path, re_path
from . import views

app_name = 'paymentoptions'

urlpatterns = [
    path('details', views.paymentoptions, name='payment'),
]
