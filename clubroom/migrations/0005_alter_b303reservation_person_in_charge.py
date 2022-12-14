# Generated by Django 3.2 on 2022-08-15 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_alter_profile_grade'),
        ('clubroom', '0004_alter_b303reservation_purpose'),
    ]

    operations = [
        migrations.AlterField(
            model_name='b303reservation',
            name='person_in_charge',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_in_charge', to='accounts.profile', verbose_name='予約者'),
        ),
    ]
