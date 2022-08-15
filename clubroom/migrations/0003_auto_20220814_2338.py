# Generated by Django 3.2 on 2022-08-14 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_alter_profile_grade'),
        ('clubroom', '0002_auto_20220814_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='b303reservation',
            name='participants',
            field=models.ManyToManyField(blank=True, to='accounts.Profile', verbose_name='参加者'),
        ),
        migrations.AlterField(
            model_name='b303reservation',
            name='person_in_charge',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_in_charge', to='accounts.profile', verbose_name='責任者'),
        ),
    ]
