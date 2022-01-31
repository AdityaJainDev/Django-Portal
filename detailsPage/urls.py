from django.urls import path
from .views import index
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='home'),
]
