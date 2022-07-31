from django.shortcuts import render

# Create your views here.


def signupfunc(request):
    if request.method == 'POST':
        print('this is POST')
    else:
        print('this is GET')
    # request, テンプレのファイル, モデルのデータを引数にとる
    return render(request, 'board/signup.html', {'some': 100})
