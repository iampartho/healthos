from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class ChangePlanForm(ModelForm):
    class Meta:
        model = User
        fields = ['plan']
        labels = {'plan': 'Please choose one of the following plan'}


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'plan', 'company',
                  'available_balance',  'password1', 'password2']
        labels = {
            'plan': 'Make a data plan',
            'available_balance': 'Starting balance',
            'company': 'Select your subscriber '
        }
