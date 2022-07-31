from django.urls import path, include
from .views import signupfunc, loginfunc

urlpatterns = [
    path('signup/', signupfunc),
    path('login/', loginfunc),
]
