from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from hellusers.models import HellUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = HellUser
        fields = ("username", "email", "person")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = HellUser
        fields = ("username", "email", "person")


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nutzerin")
    password = forms.CharField(
        widget=forms.PasswordInput, max_length=100, label="Password"
    )
    email = forms.CharField(max_length=100, label="Mail")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-row p-3 mt-4 mb-4 border bg-light form-inline"
        self.helper.field_class = "col-auto"
        self.helper.form_method = "post"
        self.helper.form_action = "adduser"
        self.helper.form_show_labels = False
        self.helper.add_input(Submit("submit", "Registrieren"))
