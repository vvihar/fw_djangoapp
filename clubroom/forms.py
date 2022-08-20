"""部室予約のフォームを管理する"""
from accounts.widgets import SuggestWidget
from django import forms
from django.urls import reverse_lazy

from .models import B303Reservation


class ReservationForm(forms.ModelForm):
    """予約用フォーム"""

    class Meta:
        """Metaクラス"""

        model = B303Reservation
        fields = (
            "title",
            "purpose",
            "date",
            "start_time",
            "end_time",
            "person_in_charge",
            "participants",
        )
        widgets = {
            "participants": SuggestWidget(
                attrs={"data-url": reverse_lazy("accounts:api_members_get")}
            ),
            "start_time": forms.TimeInput(format="%H:%M"),
            "end_time": forms.TimeInput(format="%H:%M"),
        }


class ReservationFormAdmin(forms.ModelForm):
    """予約用フォーム(管理者用)"""

    class Meta:
        """Metaクラス"""

        model = B303Reservation
        fields = "__all__"
        widgets = {
            "participants": SuggestWidget(
                attrs={"data-url": reverse_lazy("accounts:api_members_get")}
            ),
            "start_time": forms.TimeInput(format="%H:%M"),
            "end_time": forms.TimeInput(format="%H:%M"),
        }
