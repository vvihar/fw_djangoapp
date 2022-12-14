# Generated by Django 3.2 on 2022-08-02 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_profile_enrolled_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='enrolled_year',
            field=models.IntegerField(choices=[('2009', '2009年度'), ('2010', '2010年度'), ('2011', '2011年度'), ('2012', '2012年度'), ('2013', '2013年度'), ('2014', '2014年度'), ('2015', '2015年度'), ('2016', '2016年度'), ('2017', '2017年度'), ('2018', '2018年度'), ('2019', '2019年度'), ('2020', '2020年度'), ('2021', '2021年度'), ('2022', '2022年度')], default=2022, verbose_name='入学年'),
        ),
    ]
