# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "autofocus": True,
            "class": "form-control",
            "placeholder": "ej: usuario@correo.com",
            "autocomplete": "email",
        })
    )
