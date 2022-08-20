"""ToolsのURLを管理する"""
from django.urls import path
from .views import index, qrcode_generator, fw_logo, PDFPageNumber

app_name = "tools"

urlpatterns = [
    path("", index, name=""),
    path("qrcode/", qrcode_generator, name="qrcode"),
    path("logo/", fw_logo, name="logo"),
    path("pdf/page_number/", PDFPageNumber.as_view(), name="pdf_page_number"),
]
