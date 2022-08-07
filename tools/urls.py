from django.urls import path
from .views import index, qr

app_name = 'tools'

urlpatterns = [
    path('', index, name=""),
    path('qrcode/', qr, name="qrcode"),
]
