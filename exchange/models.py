from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  balance_usd = models.DecimalField(
      max_digits=12, decimal_places=2, default=1000.00
  )
  balance_bdt = models.DecimalField(
      max_digits=12, decimal_places=2, default=50000.00
  )


class Transaction(models.Model):
  METHOD_CHOICES = [('bKash', 'bKash'), ('Bank', 'Bank Transfer')]
  TYPE_CHOICES = [('Deposit', 'Deposit'), ('Withdraw', 'Withdraw')]

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  method = models.CharField(max_length=20, choices=METHOD_CHOICES)
  tx_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
  account_number = models.CharField(max_length=50)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return (
        f'{self.user.username} - {self.tx_type} {self.amount} via'
        f' {self.method}'
    )