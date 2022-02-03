from django.db import models
from django import forms

class SepaModel(models.Model):
    account_number = models.CharField(max_length = 100, blank=True)
    owner = models.CharField(max_length = 100)
    sort_code = models.CharField(max_length = 100)
    bank = models.CharField(max_length=100)
 
    def __str__(self):
        return f"Sepa Payment by {self.owner}"