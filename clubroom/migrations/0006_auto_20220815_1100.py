# Generated by Django 3.2 on 2022-08-15 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubroom', '0005_alter_b303reservation_person_in_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='b303reservation',
            name='end_datetime',
            field=models.DateTimeField(null=True, verbose_name='終了日時'),
        ),
        migrations.AddField(
            model_name='b303reservation',
            name='start_datetime',
            field=models.DateTimeField(null=True, verbose_name='開始日時'),
        ),
    ]
