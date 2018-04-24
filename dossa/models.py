from django.db import models

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="")
    link = models.CharField(max_length=300, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
