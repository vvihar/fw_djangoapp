from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# QR Code Generator
from PIL import Image
import qrcode
import base64
from io import BytesIO
from .forms import QRcodeForm


# Create your views here.

@login_required
def index(request):
    return render(request, 'tools/index.html')


# QR Code Generator
@login_required
def qr(request):
    form = QRcodeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            content = form.cleaned_data["content"]
            bgcolor = form.cleaned_data["bgcolor"]
            qrcolor = form.cleaned_data["qrcolor"]
            qr = qrcode.QRCode(
                box_size=15,
                border=4,
            )
            qr.add_data(content)
            qr.make(fit=True)
            qrcode_img = qr.make_image(fill_color=qrcolor, back_color=bgcolor)
            buffer = BytesIO()
            qrcode_img.save(buffer, format="PNG")
            qrcode_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            context = {
                "qr": qrcode_base64,
                "content": content,
                "form": form,
                "bgcolor": bgcolor,
                "qrcolor": qrcolor,
            }
        else:
            messages.error(request, '入力に誤りがあります。')
            context = {
                "form": form,
            }
    else:
        context = {
            "form": form,
            "qrcolor": "#000000",
            "bgcolor": "#FFFFFF",
        }
    return render(request, 'tools/qrcode.html', context)


@login_required
def fw_logo(request):
    return render(request, 'tools/logo.html')
# このアプリは実質的に Python ではなく、JavaScript で動いている
# Django はページを返すだけで、特別な処理は何もしていない
