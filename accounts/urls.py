from django.urls import path, include
from .views import signupfunc, profileupdatefunc
from django.contrib.auth.views import PasswordChangeView

app_name = 'accounts'

urlpatterns = [
    # django.contrib.auth.urls に含まれない機能を実装
    # サインアップ、登録情報の変更は含まれない
    path('index/', signupfunc, name=''),
    path('signup/', signupfunc, name="signup"),
    path('update/', profileupdatefunc, name="update"),
    path('password_change/', PasswordChangeView.as_view(template_name='registration/password_change.html'), name="password_change"),
    path('password_change/done/', PasswordChangeView.as_view(template_name='registration/password_change_done.html'), name="password_change_done"),
    path('', include('django.contrib.auth.urls')),
]
