from distutils.log import error
from email.policy import default
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
    bgcolor = forms.CharField(
        max_length=255,
        required=True,
        label="背景色",
        initial="#FFFFFF",
    )
    qrcolor = forms.CharField(
        max_length=15,
        required=True,
        label="QRコードの色",
        initial="#000000",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bgcolor'].widget = forms.HiddenInput()
        self.fields['qrcolor'].widget = forms.HiddenInput()
