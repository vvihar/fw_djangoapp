from django.db import models

# Create your models here.


class TodoModel(models.Model):
    CHOICE = ('danger', 'High'), ('warning', 'Normal'), ('primary', 'Low')
    title = models.CharField(max_length=100)
    memo = models.TextField()
    priority = models.CharField(max_length=10, choices=CHOICE)
    duedate = models.DateField()

    def __str__(self):
        return self.title
