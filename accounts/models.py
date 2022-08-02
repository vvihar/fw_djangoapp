from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class Group(models.Model):
    group_name = models.CharField(
        "班名",
        max_length=10,
        unique=True,
    )

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = '班'
        verbose_name_plural = '班'


class Division(models.Model):
    division = models.CharField(
        "担当名",
        max_length=30,
        unique=True,
    )

    def __str__(self):
        return self.division

    class Meta:
        verbose_name = '担当'
        verbose_name_plural = '担当'


# Django 標準のユーザー管理機能における User モデルを拡張する
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
        related_name="profile",
    )

    COURSE_CHOICES = (
        ('s1', '理科一類'),
        ('s2', '理科二類'),
        ('s3', '理科三類'),
        ('l1', '文科一類'),
        ('l2', '文科二類'),
        ('l3', '文科三類'),
    )
    course = models.CharField(
        verbose_name="科類",
        max_length=4,
        choices=COURSE_CHOICES,
        default=None,
    )

    FACULTY_CHOICES = (
        ('法', '法学部'),
        ('医', '医学部'),
        ('工', '工学部'),
        ('文', '文学部'),
        ('理', '理学部'),
        ('農', '農学部'),
        ('経', '経済学部'),
        ('教養', '教養学部'),
        ('教育', '教育学部'),
        ('薬', '薬学部'),
    )
    faculty = models.CharField(
        verbose_name="学部",
        max_length=2,
        choices=FACULTY_CHOICES,
        null=True,
        blank=True,
    )
    department = models.CharField(
        verbose_name="学科",
        max_length=30,
        null=True,
        blank=True,
    )

    ENROLLED_YEAR_CHOICES = (
        (i, str(i)+"年度")
        for i in range(2009, datetime.today().year+1)
    )
    enrolled_year = models.IntegerField(
        verbose_name="入学年度",
        default=datetime.today().year,
        choices=ENROLLED_YEAR_CHOICES,
    )

    max_grade = datetime.today().year - 2009  # 最も若い期
    GRADE_CHOICES = ((str(i)+"期", str(i)+"期") for i in range(0, max_grade+1))
    grade = models.CharField(
        verbose_name="期",
        max_length=3,
        choices=GRADE_CHOICES,
        default=str(max_grade)+"期",
    )

    SEX_CHOICES = (
        ("未回答", "回答しない"),
        ("男", "男"),
        ("女", "女"),
    )
    sex = models.CharField(
        verbose_name="性別",
        max_length=5,
        choices=SEX_CHOICES,
        default=None,
    )

    group = models.ForeignKey(
        Group,  # Group Class を継承
        verbose_name=("班"),
        on_delete=models.SET_NULL,  # 班が削除されたら、メンバーの班欄を空白にする
        default=None,
        null=True,
        blank=True
    )

    division = models.ForeignKey(
        Division,  # Division Class を継承
        verbose_name=("担当"),
        on_delete=models.SET_NULL,  # 担当が削除されたら、メンバーの担当欄を空白にする
        default=None,
        null=True,
        blank=True
    )

    def __str__(self):
        if self.user.last_name and self.user.first_name:
            return self.user.last_name + " " + self.user.first_name  # 管理画面に表示する名前（姓＋名）
        else:
            return self.user.username  # 姓名が未設定であれば、ユーザー名を返す
        # user は Django 標準のユーザー管理機能から継承しているもの

    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'


'''
データベース関連のコードを更新したら、
python manage.py makemigrations
python manage.py migrate
でデータベースを更新する
（これは user 周りに限らず、他のアプリの models.py に関してもそう）
'''