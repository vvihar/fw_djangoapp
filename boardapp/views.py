from audioop import reverse
from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

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
    return render(request, 'board/signup.html', {})


def loginfunc(request):
    if request.method == 'POST':
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:  # user がいる場合
                login(request, user)
                # login 成功
                return redirect('list')  # list ページにリダイレクト
            else:
                # login 失敗
                return render(request, 'board/login.html', {})
    # ただのアクセス
    return render(request, 'board/login.html', {})

# render: 受け取った情報を組み合わせてページを表示
# redirect: 別のビューを返す


@login_required  # decorator: 関数が呼び出される前に処理される内容
def listfunc(request):
    object_list = BoardModel.objects.all()
    return render(request, 'board/list.html', {'object_list': object_list})

# Login 状態の確認は、HTML の if user.is_authenticated でも可能


def logoutfunc(request):
    logout(request)
    return redirect('login')


def detailfunc(request, pk):
    object = get_object_or_404(BoardModel, pk=pk)
    return render(request, 'board/detail.html', {'object': object})


def goodfunc(request, pk):
    # object = get_object_or_404(BoardModel, pk=pk) # <-この記法でも良い
    object = BoardModel.objects.get(pk=pk)
    object.good += 1
    object.save()
    return redirect('list')


def readfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    username = request.user.get_username()
    if username in object.readtext:
        pass
    else:
        object.read += 1
        object.readtext += ' ' + username
        object.save()
    return redirect('list')


class BoardCreate(CreateView):
    template_name = 'board/create.html'
    model = BoardModel
    fields = ['title', 'content', 'author', 'sns_image']
    success_url = reverse_lazy('list')
