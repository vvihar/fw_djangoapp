from django.contrib import admin
from .models import B303Reservation
from .forms import ReservationFormAdmin

# Register your models here.


class B303ReservationAdmin(admin.ModelAdmin):
    form = ReservationFormAdmin


admin.site.register(B303Reservation, B303ReservationAdmin)
