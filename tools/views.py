from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import os
import tempfile
from urllib import request
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView

from .forms import QRcodeForm, PDFPageNumberForm

# QR Code Generator
from PIL import Image
import qrcode
import base64
from io import BytesIO

# for Handling PDF Files
from pagelabels import PageLabels, PageLabelScheme
from pdfrw import PdfReader, PdfWriter
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from pdfrw import PdfReader
from reportlab.pdfgen.canvas import Canvas

# Create your views here.


# @login_required
def index(request):
    return render(request, 'tools/index.html')


# QR Code Generator
# @login_required
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


# Logo Generator
# @login_required
def fw_logo(request):
    return render(request, 'tools/logo.html')
# このアプリは実質的に Python ではなく、JavaScript で動いている
# Django はページを返すだけで、特別な処理は何もしていない


# PDF Page Number


class PDFPageNumber(FormView):
    template_name = 'tools/pdf_page_number.html'
    form_class = PDFPageNumberForm

    def form_valid(self, form):
        with tempfile.TemporaryDirectory() as tempdir:
            pdf = form.cleaned_data['pdf']
            start_from = form.cleaned_data['start_from']
            if not start_from:
                start_from = 1
            end_at = form.cleaned_data['end_at']
            title = form.cleaned_data['title']
            margin_bottom = form.cleaned_data['margin_bottom']
            font_size = form.cleaned_data['font_size']
            if start_from < 1:
                messages.error(self.request, 'ページ番号の開始ページは1以上の数字を入力してください。')
                return super().form_invalid(form)
            if margin_bottom < 0:
                messages.error(self.request, 'ページ下部の余白は0以上の数字を入力してください。')
                return super().form_invalid(form)
            if font_size < 0:
                messages.error(self.request, 'フォントサイズは0以上の数字を入力してください。')
                return super().form_invalid(form)
            if end_at and end_at < start_from:
                messages.error(self.request, '終了ページは開始ページより大きい数字を入力してください。')
                return super().form_invalid(form)
            filename = str(pdf).replace('.pdf', '_new.pdf')
            path = os.path.join(tempdir, filename)  # 一時的に保存するファイルのパス
            reader = PdfReader(pdf)
            pdf_new = path
            pages = [pagexobj(page) for page in reader.pages]

            canvas = Canvas(pdf_new)
            # PDF のメタデータを設定する
            canvas.setAuthor("FairWind Portal Document Service")
            canvas.setTitle(title)
            canvas.setSubject("")  # 必要であれば設定

            for page_num, page in enumerate(pages, 1):
                canvas.setPageSize((page.BBox[2], page.BBox[3]))
                canvas.doForm(makerl(canvas, page))

                if page_num < start_from:
                    page_num = ''
                elif end_at and page_num > end_at:
                    page_num = ''
                else:
                    page_num = page_num - start_from + 1
                footer_text = str(page_num)
                canvas.saveState()
                canvas.setStrokeColorRGB(0, 0, 0)
                canvas.setFont("Helvetica", font_size)
                page_width = page.BBox[2] - page.BBox[0]
                text_width = canvas.stringWidth(footer_text, "Helvetica", 11)
                canvas.drawString(page_width / 2 - text_width / 2, margin_bottom, footer_text)
                canvas.restoreState()
                canvas.showPage()
            canvas.save()

            response = StreamingHttpResponse(
                FileWrapper(open(path, 'rb'), 8192),
                content_type='application/pdf'
            )
            # ファイル名を指定して、ダウンロードを強制
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response
