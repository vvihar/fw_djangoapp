from django.shortcuts import render
from django.contrib import messages

# QR Code Generator
from PIL import Image
import qrcode
import base64
from io import BytesIO
from .forms import QRcodeForm

# Create your views here.


def index(request):
    return render(request, 'tools/index.html')


# QR Code Generator
def qr(request):
    form = QRcodeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            content = form.cleaned_data["content"]
            qrcode_img = qrcode.make(content, box_size=15)
            buffer = BytesIO()
            qrcode_img.save(buffer, format="PNG")
            qrcode_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            context = {
                "qr": qrcode_base64,
                "content": content,
                "form": form,
            }
        else:
            messages.error(request, '入力に誤りがあります。')
            context = {
                "form": form,
            }
    else:
        context = {
            "form": form,
        }
    return render(request, 'tools/qrcode.html', context)
