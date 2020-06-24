from django.db import models


class Paper(models.Model):
    title = models.CharField(max_length=30)
    authors = models.CharField(max_length=30)
    keywords = models.CharField(max_length=30)
    status = models.CharField(max_length=30, default='در دست بررسی')
    paper = models.FileField(upload_to='papers')

    def __str__(self):
        return self.title
