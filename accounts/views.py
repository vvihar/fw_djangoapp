from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm, UserCreateForm, UpdateProfileForm, UpdateUserForm
from .models import Profile
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.


def signupfunc(request):
    user_form = UserCreateForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():

        # Userモデルの処理。ログインできるようis_activeをTrueにし保存
        user = user_form.save(commit=False)
        user.is_active = True
        user.save()

        # Profileモデルの処理。↑のUserモデルと紐づける
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        return redirect("boardapp:")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def profileupdatefunc(request):
    info = ""
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST or None, instance=request.user)
        profile_form = UpdateProfileForm(request.POST or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            context = {
                "user_form": user_form,
                "profile_form": profile_form,
                "info": "更新しました。",
            }
            return render(request, "accounts/update.html", context)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        messages.error(request, "フォームが不正です。")
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "accounts/update.html", context)
