from django.urls import path
from .views import index, reservation, reservationUpdate, reservationCancel
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required

app_name = 'clubroom'

urlpatterns = [
    # django.contrib.auth.urls に含まれない機能を実装
    path('', index, name=''),
    path('new/', reservation.as_view(), name='reservation'),
    path('<int:pk>/update/', reservationUpdate.as_view(), name='reservation_update'),
    path('<int:pk>/cancel/', reservationCancel.as_view(), name='reservation_cancel'),
]
