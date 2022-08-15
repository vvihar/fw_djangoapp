from django.db import models
from accounts.models import Profile

# Create your models here.


class B303Reservation(models.Model):
    title = models.CharField(
        max_length=30,
        verbose_name="タイトル",
    )
    purpose = models.CharField(
        max_length=255,
        verbose_name="目的",
        null=True,
        blank=True,
    )
    date = models.DateField(verbose_name="日付")
    start_time = models.TimeField(verbose_name="開始時刻")
    end_time = models.TimeField(verbose_name="終了時刻")
    start_datetime = models.DateTimeField(verbose_name="開始日時", null=True)
    end_datetime = models.DateTimeField(verbose_name="終了日時", null=True)
    person_in_charge = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        verbose_name="予約者",
        null=True,
        related_name="person_in_charge",
    )
    participants = models.ManyToManyField(Profile, verbose_name='参加者', blank=True)

    def __str__(self):
        return self.date.strftime('%Y/%m/%d') + ' ' + self.start_time.strftime('%H:%M') + '-' + self.end_time.strftime('%H:%M') + '（' + self.title + '）'

    class Meta:
        verbose_name = '部室予約'
        verbose_name_plural = '部室予約'
