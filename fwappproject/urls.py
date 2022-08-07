"""fwappproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import memberview, helloWorldView  # views.pyから関数をimport
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('members/', memberview),  # memberview関数を呼び出す (function based view)
    # helloWorldViewを呼び出す (class based view)
    path('helloworld/', helloWorldView.as_view()),
    path('app/', include('helloworldapp.urls')),
    path('todo/', include('todo.urls'), name="todoapp"),
    path('board/', include('boardapp.urls'), name="boardapp"),
    path('accounts/', include('accounts.urls'), name="accounts"),
    path('tools/', include('tools.urls'), name="tools"),
    # TODO: tool app を作成する
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
