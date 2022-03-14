from django.contrib.auth.backends import ModelBackend
import requests
from django.conf import settings
from django.contrib.auth.models import User

class CustomerBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        knr = kwargs['username']
        password = kwargs['password']
        try:
            data = requests.get(settings.CRM_ENDPOINT + "Kunden/Login/", auth=(knr, password)).json()
            request.session['username'] = data["data"]["knr"]
            request.session['password'] = password
            request.session['name'] = data["data"]["kunde_name"]
            if data["status"]  == 1:
                try:
                    user = User.objects.get(username=data["data"]["knr"])
                    if user.is_active:
                        return user
                except Exception as e:
                    user = User.objects.create_user(username=data["data"]["knr"])
                    return user
        except Exception as e:
            print(e)