from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Transaction


class UserRegisterForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ['username', 'email', 'password']
    widgets = {
        'username': forms.TextInput(
            attrs={
                'class': 'w-full p-2 bg-gray-700 rounded text-white',
                'placeholder': '8 to 32 characters',
            }
        ),
        'email': forms.EmailInput(
            attrs={'class': 'w-full p-2 bg-gray-700 rounded text-white'}
        ),
    }

  def clean_username(self):
    username = self.cleaned_data.get('username')
    if len(username) < 8 or len(username) > 32:
      raise ValidationError(
          'Username must be between 8 and 32 characters long.'
      )
    return username


class DepositForm(forms.ModelForm):

  class Meta:
    model = Transaction
    fields = ['method', 'amount', 'account_number']
    widgets = {
        'method': forms.Select(
            attrs={'class': 'w-full p-2 bg-gray-700 rounded text-white'}
        ),
        'amount': forms.NumberInput(
            attrs={'class': 'w-full p-2 bg-gray-700 rounded text-white'}
        ),
        'account_number': forms.TextInput(
            attrs={
                'class': 'w-full p-2 bg-gray-700 rounded text-white',
                'placeholder': 'Enter bKash/Bank Account No',
            }
        ),
    }