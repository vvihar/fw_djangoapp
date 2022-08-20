"""Accountsのフォームを管理する"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        """Metaクラス"""

        model = User
        fields = ("username", "last_name", "first_name", "password1", "password2")


class ProfileForm(forms.ModelForm):
    """プロフィール登録用フォーム"""

    class Meta:
        """Metaクラス"""

        model = Profile
        fields = (
            "email",
            "course",
            "enrolled_year",
            "grade",
            "sex",
        )


class UpdateUserForm(forms.ModelForm):
    """ユーザー編集用フォーム"""

    class Meta:
        """Metaクラス"""

        model = User
        fields = ("email",)


class UpdateProfileForm(forms.ModelForm):
    """プロフィール編集用フォーム"""

    class Meta:
        """Metaクラス"""

        model = Profile
        fields = (
            "email",
            "course",
            "enrolled_year",
            "grade",
            "sex",
            "faculty",
            "department",
            "group",
            "division",
        )


class CSVUploadForm(forms.Form):
    """ユーザー一括登録フォーム"""

    file = forms.FileField(label="CSVファイル", help_text="CSV形式のファイルをアップロードしてください。")
