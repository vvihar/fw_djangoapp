from django.urls import path, include
from .views import signupfunc, profileupdatefunc, indexfunc, GroupList, GroupCreate, GroupDelete, GroupUpdate
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required

app_name = 'accounts'

urlpatterns = [
    # django.contrib.auth.urls に含まれない機能を実装
    path('', indexfunc, name=''),
    path('signup/', signupfunc, name="signup"),
    path('update/', profileupdatefunc, name="update"),
    path('password_change/', PasswordChangeView.as_view(template_name='accounts/password_change.html', success_url=reverse_lazy('accounts:password_change_done')), name="password_change"),
    path('password_change/done/', PasswordChangeView.as_view(template_name='accounts/password_change_done.html'), name="password_change_done"),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),

    path('group/', staff_member_required(GroupList.as_view(), login_url='accounts:login'), name="group"),
    path('group/create/', staff_member_required(GroupCreate.as_view(), login_url='accounts:login'), name="group_create"),
    path('group/<int:pk>/delete/', staff_member_required(GroupDelete.as_view(), login_url='accounts:login'), name="group_delete"),
    path('group/<int:pk>/update/', staff_member_required(GroupUpdate.as_view(), login_url='accounts:login'), name="group_update"),
]
