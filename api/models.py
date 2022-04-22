from django.contrib.auth.models import User
from django.db import models

from .utils import create_new_iban_number


class Bank(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return self.name + ' - ' + self.address

    class Meta:
        db_table = 'Bank'


class Account(models.Model):
    title = models.CharField(max_length=50, null=False, db_column='title')
    IBAN = models.CharField(max_length=10, null=False, editable=False, unique=True, default=create_new_iban_number,
                            db_column='IBAN')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_column='owner')
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, db_column='bank')
    balance = models.FloatField(null=False, default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'Account'
