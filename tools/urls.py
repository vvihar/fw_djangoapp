from django.urls import path
from .views import index, qr, fw_logo

app_name = 'tools'

urlpatterns = [
    path('', index, name=""),
    path('qrcode/', qr, name="qrcode"),
    path('logo/', fw_logo, name="logo"),
]
