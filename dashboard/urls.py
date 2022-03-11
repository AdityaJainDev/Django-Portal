from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('home/', views.index, name='home'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('change_password/', views.change_password, name='change_password'),
]
