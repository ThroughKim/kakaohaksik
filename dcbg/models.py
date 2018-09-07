from django.db import models

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=100, default="")
    content = models.TextField()
    time = models.DateTimeField()