from django.shortcuts import render, redirect
from .forms import ProfileForm, UserCreateForm, UpdateProfileForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from .models import Group, Division
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

# Create your views here.

@staff_member_required(login_url='accounts:login')
def signupfunc(request):
    user_form = UserCreateForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():

        # Userモデルの処理。ログインできるようis_activeをTrueにし保存
        user = user_form.save(commit=False)
        user.is_active = True

        # Profileモデルの処理。↑のUserモデルと紐づける
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()

        user.email = profile.email
        user.save()

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
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            profile.save()
            user.email = profile.email
            user.save()
            context = {
                "user_form": user_form,
                "profile_form": profile_form,
                "info": "更新しました。",
            }
            return render(request, "accounts/update.html", context)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "accounts/update.html", context)

@login_required
def indexfunc(request):
    alerts = []
    senior_division_year = datetime.today().year - 2
    if not request.user.profile.faculty and request.user.profile.enrolled_year <= senior_division_year:
        alerts.append("後期課程の進学先の情報を登録してください。")
    if not request.user.profile.group:
        alerts.append("所属している班の情報を登録してください。")
    if not request.user.profile.division:
        alerts.append("所属している担当の情報を登録してください。")
    context = {
        "alerts": alerts
    }
    return render(request, "accounts/index.html", context)

class GroupList(ListView):
    template_name = 'accounts/group/list.html'
    model = Group

class GroupCreate(CreateView):
    template_name = 'accounts/group/create.html'
    model = Group
    fields = ('name',)
    success_url = reverse_lazy('accounts:group')

class GroupDelete(DeleteView):
    template_name = 'accounts/group/delete.html'
    model = Group
    success_url = reverse_lazy('accounts:group')  # 成功時の遷移先

class GroupUpdate(UpdateView):
    template_name = 'accounts/group/create.html'
    model = Group
    fields = ('name',)
    success_url = reverse_lazy('accounts:group')
