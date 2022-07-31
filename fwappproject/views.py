from django.http import HttpResponse
from django.views.generic import TemplateView


def memberview(request):  # 基本的にはrequestを引数にとる
    returnobject = HttpResponse('<h1>Hello, world!</h1>')
    return returnobject


class helloWorldView(TemplateView):
    template_name = 'helloworld.html'
