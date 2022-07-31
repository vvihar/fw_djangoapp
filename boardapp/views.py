from django.shortcuts import render

# Create your views here.


def signupfunc(request):
    # request, テンプレのファイル, モデルのデータを引数にとる
    return render(request, 'board/signup.html', {'some': 100})
