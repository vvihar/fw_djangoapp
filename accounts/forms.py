from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username", "last_name", "first_name", "password1", "password2"
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "email", "course", "enrolled_year", "grade", "sex",
        )


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
        )


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "email", "course", "enrolled_year", "grade", "sex", "faculty", "department", "group", "division"
        )
