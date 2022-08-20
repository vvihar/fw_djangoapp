"""部室予約のURLを管理する"""
from django.urls import path
from .views import index, Reservation, ReservationUpdate, ReservationCancel

app_name = "clubroom"

urlpatterns = [
    # django.contrib.auth.urls に含まれない機能を実装
    path("", index, name=""),
    path("new/", Reservation.as_view(), name="reservation"),
    path("<int:pk>/update/", ReservationUpdate.as_view(), name="reservation_update"),
    path("<int:pk>/cancel/", ReservationCancel.as_view(), name="reservation_cancel"),
]
