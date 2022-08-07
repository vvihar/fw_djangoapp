from distutils.log import error
from django import forms


class QRcodeForm(forms.Form):
    content = forms.CharField(
        max_length=255,
        required=True,
        label="テキストを入力",
        error_messages={
            "required": "テキストを入力してください。",
        },
    )
