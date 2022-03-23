from django.urls import path, re_path
from .views import index
from . import views

app_name = 'paymentoptions'

urlpatterns = [
    path('', views.index, name='home'),
    path('details', views.paymentoptions, name='payment'),
]
