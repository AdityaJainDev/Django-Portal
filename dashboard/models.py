from django.db import models

# Create your models here.
class APIData(models.Model):
    account_number = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.account_number