from django.urls import path, include
from .views import signupfunc

urlpatterns = [
    path('signup/', signupfunc),
]
