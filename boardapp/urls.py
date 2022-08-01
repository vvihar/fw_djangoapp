from django.urls import path, include
from .views import signupfunc, loginfunc, listfunc, logoutfunc

urlpatterns = [
    path('', listfunc),
    path('signup/', signupfunc, name="signup"),
    path('login/', loginfunc, name="login"),
    path('list/', listfunc, name="list"),
    path('logout/', logoutfunc, name="logout")
]
