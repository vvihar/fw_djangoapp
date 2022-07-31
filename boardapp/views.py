from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login

# Create your views here.


def signupfunc(request):
    # print(request.POST)
    if request.method == 'POST':
        username = request.POST['username']  # name属性を使用
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, '', password)
            return render(request, 'board/signup.html', {})
        except IntegrityError:  # 重複したユーザー名の場合
            return render(request, 'board/signup.html', {'error': 'このユーザー名は既に使用されています'})
    # request, テンプレのファイル, モデルのデータを引数にとる
    return redirect('login')


def loginfunc(request):
    if request.method == 'POST':
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:  # user がいる場合
                login(request, user)
                # login 成功
                return render(request, 'board/login.html', {'context': 'logged in'})
            else:
                # login 失敗
                return render(request, 'board/login.html', {'context': 'not logged in'})
    # ただのアクセス
    return render(request, 'board/login.html', {'context': 'get method'})

# render: 受け取った情報を組み合わせてページを表示
# redirect: 別のビューを返す


def listfunc(request):
    return render(request, 'board/list.html', {})
