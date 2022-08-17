from multiprocessing import context
from django.urls import reverse
from urllib.parse import urlencode
from django.utils.timezone import make_aware
import datetime
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservationForm
from .models import B303Reservation
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone


# Create your views here.


@login_required
def index(request):
    # アクセス時に過去の予約を削除
    today = datetime.date.today()
    events_delete = B303Reservation.objects.filter(date__lt=today)
    for event in events_delete:
        event.delete()
    events_list = B303Reservation.objects.all().order_by('start_datetime')
    context = {
        'events_list': events_list,
    }
    return render(request, 'clubroom/index.html', context)


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        reservation = B303Reservation.objects.get(pk=self.kwargs['pk'])
        return user.is_staff or reservation.person_in_charge == user.profile

    def handle_no_permission(self):
        redirect_url = reverse('accounts:login')
        # パラメータのdictをurlencodeする。複数のパラメータを含めることも可能
        parameters = urlencode({'next': self.request.path})
        # URLにパラメータを付与する
        url = f'{redirect_url}?{parameters}'
        return redirect(url)


class reservation(LoginRequiredMixin,  CreateView):
    template_name = 'clubroom/new.html'
    model = B303Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('clubroom:')

    def form_valid(self, form):
        reservation = form.save(commit=False)
        reservation.start_datetime = make_aware(
            datetime.datetime.combine(reservation.date, reservation.start_time))
        reservation.end_datetime = make_aware(
            datetime.datetime.combine(reservation.date, reservation.end_time))
        if reservation.start_datetime >= reservation.end_datetime:
            messages.error(self.request, '開始時刻は終了時刻よりも前に設定してください。')
            return super().form_invalid(form)
        # 過去の日時を予約していないかチェックする
        now = timezone.now()
        if reservation.start_datetime < now:
            messages.error(self.request, '過去の日時は予約できません。')
            return super().form_invalid(form)
        # 既存の予約との競合をチェックする
        date = reservation.date
        for existing_reservation in B303Reservation.objects.filter(date=date):
            if reservation.start_time < existing_reservation.end_time and reservation.end_time > existing_reservation.start_time and existing_reservation.pk != reservation.pk:
                messages.error(self.request, '「' + existing_reservation.title + '」と予約の時間が重複しています。')
                return super().form_invalid(form)
        form.save()
        messages.success(self.request, '予約が完了しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '入力に誤りがあります。')
        return super().form_invalid(form)


class reservationUpdate(LoginRequiredMixin, OnlyYouMixin, UpdateView):
    template_name = 'clubroom/update.html'
    model = B303Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('clubroom:')

    def form_valid(self, form):
        reservation = form.save(commit=False)
        reservation.start_datetime = make_aware(
            datetime.datetime.combine(reservation.date, reservation.start_time))
        reservation.end_datetime = make_aware(
            datetime.datetime.combine(reservation.date, reservation.end_time))
        if reservation.start_datetime >= reservation.end_datetime:
            messages.error(self.request, '開始時刻は終了時刻よりも前に設定してください。')
            return super().form_invalid(form)
        # 過去の日時を予約していないかチェックする
        now = timezone.now()
        if reservation.start_datetime < now:
            messages.error(self.request, '過去の日時は予約できません。')
            return super().form_invalid(form)
        # 既存の予約との競合をチェックする
        date = reservation.date
        for existing_reservation in B303Reservation.objects.filter(date=date):
            if reservation.start_time < existing_reservation.end_time and reservation.end_time > existing_reservation.start_time and existing_reservation.pk != reservation.pk:
                messages.error(self.request, '「' + existing_reservation.title + '」と予約の時間が重複しています。')
                return super().form_invalid(form)
        form.save()
        messages.success(self.request, '予約を変更しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.cleaned_data)
        messages.error(self.request, '入力に誤りがあります。')
        return super().form_invalid(form)


class reservationCancel(LoginRequiredMixin, OnlyYouMixin, DeleteView):
    model = B303Reservation
    success_url = reverse_lazy('clubroom:')
    template_name = 'clubroom/cancel.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '予約が削除されました。')
        return super().delete(request, *args, **kwargs)
