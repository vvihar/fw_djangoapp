from django import forms
from django.urls import reverse_lazy
from .models import B303Reservation
from accounts.widgets import SuggestWidget


class ReservationForm(forms.ModelForm):
    class Meta:
        model = B303Reservation
        fields = 'title', 'purpose', 'date', 'start_time', 'end_time', 'person_in_charge', 'participants'
        widgets = {
            'participants': SuggestWidget(attrs={'data-url': reverse_lazy('accounts:api_members_get')}),
            'start_time': forms.TimeInput(format='%H:%M'),
            'end_time': forms.TimeInput(format='%H:%M'),
        }


class ReservationFormAdmin(forms.ModelForm):
    class Meta:
        model = B303Reservation
        fields = '__all__'
        widgets = {
            'participants': SuggestWidget(attrs={'data-url': reverse_lazy('accounts:api_members_get')}),
            'start_time': forms.TimeInput(format='%H:%M'),
            'end_time': forms.TimeInput(format='%H:%M'),
        }
