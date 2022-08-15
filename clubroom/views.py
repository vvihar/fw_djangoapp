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


# Create your views here.


@login_required
def index(request):
    events_list = B303Reservation.objects.all()
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
    template_name = 'clubroom/reservation.html'
    model = B303Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('clubroom:')

    def form_valid(self, form):
        #FIXME: 予約の競合がないかをチェック
        reservation = form.save(commit=False)
        reservation.start_datetime = datetime.datetime.combine(
            reservation.date, reservation.start_time)
        reservation.end_datetime = datetime.datetime.combine(reservation.date, reservation.end_time)
        form.save()
        messages.success(self.request, '予約が完了しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.cleaned_data)
        messages.error(self.request, '入力に誤りがあります。')
        return super().form_invalid(form)


class reservationUpdate(LoginRequiredMixin, OnlyYouMixin, UpdateView):
    template_name = 'clubroom/update.html'
    model = B303Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('clubroom:')

    def form_valid(self, form):
        #FIXME: 予約の競合がないかをチェック
        reservation = form.save(commit=False)
        reservation.start_datetime = make_aware(
            datetime.datetime.combine(reservation.date, reservation.start_time))
        reservation.end_datetime = make_aware(
            datetime.datetime.combine(reservation.date, reservation.end_time))
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
