# Generated by Django 3.2 on 2022-08-02 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_profile_enrolled_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(choices=[('未回答', '回答しない'), ('男', '男'), ('女', '女')], default=None, max_length=5, verbose_name='性別'),
        ),
    ]
