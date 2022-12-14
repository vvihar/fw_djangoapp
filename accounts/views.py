"""Accountsのビューを管理する"""
import csv
import io
from datetime import datetime

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import (
    CSVUploadForm,
    ProfileForm,
    UpdateProfileForm,
    UpdateUserForm,
    UserCreateForm,
)
from .models import Division, Group, Profile

# Create your views here.


@staff_member_required(login_url="accounts:login")
def signup(request):
    """新規登録"""
    user_form = UserCreateForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user = user_form.save(commit=False)
        user.is_active = True
        user.save()

        # Profile モデルの処理。↑の User モデルと紐づける
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()

        user.email = profile.email  # User モデルの email に Profile モデルの email をそのまま転写
        user.save()

        return redirect("accounts:")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "accounts/signup.html", context)


@login_required
def profile_update(request):
    """プロフィール更新"""
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST or None, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST or None, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            profile.save()
            user.email = profile.email
            user.save()
            messages.success(request, "ユーザー情報を更新しました。")
            context = {
                "user_form": user_form,
                "profile_form": profile_form,
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
def index(request):
    """トップページ"""
    senior_division_year = datetime.today().year - 2
    if (
        not request.user.profile.faculty
        and request.user.profile.enrolled_year <= senior_division_year
    ):
        messages.warning(request, "後期課程の進学先の情報を登録してください。")
    if not request.user.profile.group:
        messages.warning(request, "所属している班の情報を登録してください。")
    if not request.user.profile.division:
        messages.warning(request, "所属している担当の情報を登録してください。")
    return render(request, "accounts/index.html", {})


class GroupList(ListView):
    """班一覧"""

    template_name = "accounts/group/list.html"
    model = Group


class GroupCreate(CreateView):
    """班登録"""

    template_name = "accounts/group/create.html"
    model = Group
    fields = ("name",)
    success_url = reverse_lazy("accounts:group")

    def form_valid(self, form):
        messages.success(self.request, form.cleaned_data["name"] + "を登録しました。")
        return super().form_valid(form)


class GroupDelete(DeleteView):
    """班削除"""

    template_name = "accounts/group/delete.html"
    model = Group
    success_url = reverse_lazy("accounts:group")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "班を削除しました。")
        return super().delete(request, *args, **kwargs)


class GroupUpdate(UpdateView):
    """班編集"""

    template_name = "accounts/group/update.html"
    model = Group
    fields = ("name",)
    success_url = reverse_lazy("accounts:group")

    def form_valid(self, form):
        messages.success(self.request, form.cleaned_data["name"] + "を編集しました。")
        return super().form_valid(form)


class DivisionList(ListView):
    """担当一覧"""

    template_name = "accounts/division/list.html"
    model = Division


class DivisionCreate(CreateView):
    """担当登録"""

    template_name = "accounts/division/create.html"
    model = Division
    fields = ("name",)
    success_url = reverse_lazy("accounts:division")

    def form_valid(self, form):
        messages.success(self.request, form.cleaned_data["name"] + "を登録しました。")
        return super().form_valid(form)


class DivisionDelete(DeleteView):
    """担当削除"""

    template_name = "accounts/division/delete.html"
    model = Division
    success_url = reverse_lazy("accounts:division")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "担当を削除しました。")
        return super().delete(request, *args, **kwargs)


class DivisionUpdate(UpdateView):
    """担当編集"""

    template_name = "accounts/division/update.html"
    model = Division
    fields = ("name",)
    success_url = reverse_lazy("accounts:division")

    def form_valid(self, form):
        messages.success(self.request, form.cleaned_data["name"] + "を編集しました。")
        return super().form_valid(form)


class UserList(ListView):
    """ユーザー一覧"""

    template_name = "accounts/user/list.html"
    model = User


class UserImport(generic.FormView):
    """ユーザー一括登録"""

    template_name = "accounts/user/import.html"
    form_class = CSVUploadForm

    def form_valid(self, form):
        errors = []
        new_users = []
        new_profiles = []
        imported_users = 0
        # csv.readerに渡すため、TextIOWrapperでテキストモードなファイルに変換
        csvfile = io.TextIOWrapper(form.cleaned_data["file"], encoding="utf-8")
        reader = csv.reader(csvfile)
        username_list = list(User.objects.values_list("username", flat=True))
        email_list = list(User.objects.values_list("email", flat=True))
        # 1行ずつ取り出し、作成していく
        for row in reader:
            for i in range(len(row)):
                row[i] = row[i].strip().strip("'").strip('"')
            user_data = {
                "username": row[0],
                "last_name": row[1],  # 姓
                "first_name": row[2],  # 名
                "email": row[3],
                "course": row[4],
                "enrolled_year": row[5],
                "grade": row[6],
                "sex": row[7],
                "group": row[8],  # 班
                "division": row[9],  # 担当
                "password": row[10],
            }
            if user_data["username"] == "":
                messages.error(self.request, "ユーザー名が空白の行が見つかりました。")
                continue
            error_count = 0
            for key, value in user_data.items():
                if value == "" and key != "group" and key != "division":  # 担当、班は空白でも OK
                    error_temp = (
                        user_data["username"] + " は、データに空白の項目が見つかったため、読み込まれませんでした。"
                    )
                    if not error_temp in errors:
                        messages.error(self.request, error_temp)
                    error_count += 1
            if error_count > 0:
                continue
            if user_data["username"] in username_list:
                messages.error(
                    self.request,
                    user_data["username"] + " は、ユーザー名が他のユーザーと重複しているため、読み込まれませんでした。",
                )
                continue
            if user_data["email"] in email_list:
                messages.error(
                    self.request,
                    user_data["username"] + " は、メールアドレスが他のユーザーと重複しているため、読み込まれませんでした。",
                )
                continue
            if user_data["group"] != "" and not user_data["group"] in list(
                Group.objects.values_list("name", flat=True)
            ):
                messages.error(
                    self.request, user_data["username"] + " は、班が存在しないため、読み込まれませんでした。"
                )
                continue
            if user_data["division"] != "" and not user_data["division"] in list(
                Division.objects.values_list("name", flat=True)
            ):
                messages.error(
                    self.request, user_data["username"] + " は、担当が存在しないため、読み込まれませんでした。"
                )
                continue
            new_user = User(
                username=user_data["username"],
                last_name=user_data["last_name"],
                first_name=user_data["first_name"],
                email=user_data["email"],
                is_staff=True,
                is_active=True,
                is_superuser=False,
            )  # 一旦 User モデルを作成
            new_user.set_password(user_data["password"])  # パスワードをセット
            new_users.append(new_user)  # User モデルを保存するためのリストに追加
            new_profile = Profile(
                email=user_data["email"],
                course=user_data["course"],
                enrolled_year=user_data["enrolled_year"],
                grade=user_data["grade"],
                sex=user_data["sex"],
            )  # 一旦 Profile モデルを作成
            if user_data["group"] != "":
                new_profile.group = Group.objects.get(name=user_data["group"])
            if user_data["division"] != "":
                new_profile.division = Division.objects.get(name=user_data["division"])
            new_profiles.append(new_profile)  # Profile モデルを保存するためのリストに追加
            imported_users += 1
        User.objects.bulk_create(new_users)  # User モデルをまとめて保存
        for profile in new_profiles:
            profile.user = User.objects.get(email=profile.email)
        Profile.objects.bulk_create(new_profiles)  # Profile モデルをまとめて保存
        if imported_users > 0:
            messages.success(self.request, str(imported_users) + " 件のユーザーを読み込みました。")
        context = {
            "form": form,
        }
        return render(self.request, "accounts/user/import.html", context)


@login_required
def api_members_get(request):
    """サジェスト候補のメンバーを JSON で返す。"""
    keyword = request.GET.get("keyword")
    if keyword:
        member_list = [
            {"pk": user.profile.pk, "name": str(user.last_name + " " + user.first_name)}
            for user in User.objects.filter(username__icontains=keyword).all()
        ]
    else:
        member_list = []
    return JsonResponse({"object_list": member_list})
