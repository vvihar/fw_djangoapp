from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.


def signupfunc(request):
    object = User.objects.get(username='yakushijin-s')  # すべての情報を格納
    print(object.email)
    if request.method == 'POST':
        print('this is POST')
    else:
        print('this is GET')
    # request, テンプレのファイル, モデルのデータを引数にとる
    return render(request, 'board/signup.html', {'some': 100})
