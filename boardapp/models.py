from django.db import models

# Create your models here.


class BoardModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=50)
    sns_image = models.ImageField(upload_to='')  # settings.pyで定められている場所なら記入不要
    good = models.IntegerField(default=0)  # いいね
    read = models.IntegerField(default=0)  # 既読
    readtext = models.TextField(default='')  # 既読の人
    # null = True, blank = True で空欄可能

    def __str__(self):
        return self.title
