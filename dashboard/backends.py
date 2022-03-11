from django.contrib.auth.backends import ModelBackend
import requests
from django.conf import settings
from django.contrib.auth.models import User

class CustomerBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        knr = kwargs['username']
        password = kwargs['password']
        try:
            data = requests.get(settings.CRM_ENDPOINT + "Login/", auth=(knr, password)).json()
            if data["status"]  == 1:
                try:
                    user = User.objects.get(username=data["data"]["knr"])
                    if user.is_active:
                        return user
                except Exception as e:
                    user = User.objects.create_user(username=data["data"]["knr"], password=password, first_name=data["data"]["kunde_name"])
                    return user
        except Exception as e:
            print(e)