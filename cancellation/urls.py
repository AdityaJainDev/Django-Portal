from django.urls import path
from .views import cancellation

app_name = "cancellation"

urlpatterns = [
    path("", cancellation.as_view(), name="cancellation")
]
