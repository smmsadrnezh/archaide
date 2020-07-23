from django.contrib.auth.models import User
from django.db import models
from django.db.models import FileField


class Architecture(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, related_name='architectures', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    owl_file = FileField(upload_to='owl', unique=True)
    axiom_count = models.IntegerField(default=0)
