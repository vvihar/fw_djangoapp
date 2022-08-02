from django.urls import path, include
from .views import signupfunc, profileupdatefunc, indexfunc
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView, PasswordChangeDoneView

app_name = 'accounts'

urlpatterns = [
    # django.contrib.auth.urls に含まれない機能を実装
    path('', indexfunc, name=''),
    path('signup/', signupfunc, name="signup"),
    path('update/', profileupdatefunc, name="update"),
    path('password_change/', PasswordChangeView.as_view(template_name='accounts/password_change.html'), name="password_change"),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name="password_change_done"),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
