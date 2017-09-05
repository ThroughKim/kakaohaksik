from django.db import models

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=30, default="")
    timestamp = models.DateTimeField(auto_now_add=True)
