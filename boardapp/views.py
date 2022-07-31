from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.


def signupfunc(request):
    # print(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username, '', password)
    # request, テンプレのファイル, モデルのデータを引数にとる
    return render(request, 'board/signup.html', {'some': 100})
