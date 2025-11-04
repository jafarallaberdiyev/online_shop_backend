from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]

        widgets = {

            "avatar": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            })
        }
