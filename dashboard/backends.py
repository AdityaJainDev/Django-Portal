from django.contrib.auth.backends import ModelBackend
import requests
from django.conf import settings
from django.contrib.auth.models import User


class CustomerBackend(ModelBackend):
    def authenticate(self, request, errors, **kwargs):
        knr_or_email = kwargs["username"]
        password = kwargs["password"]

        data = requests.get(
            settings.CRM_ENDPOINT + "Kunden/Login/", auth=(knr_or_email, password)
        )
        data.raise_for_status()

        request.session["username"] = data.json()["data"]["knr"]
        request.session["password"] = password
        request.session["name"] = data.json()["data"]["kunde_name"]
        request.session["email"] = knr_or_email
        if data.json()["status"] == 1:
            try:
                user = User.objects.get(username=data.json()["data"]["knr"])
                if user.is_active:
                    return user
            except Exception as e:
                user = User.objects.create_user(username=data.json()["data"]["knr"])
                return user
