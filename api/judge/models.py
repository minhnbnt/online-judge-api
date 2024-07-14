from uuid import uuid5

from django.db import models


# Create your models here.
class Submission(models.Model):
    id = models.IntegerField(primary_key=True)
    secret = models.UUIDField(default=uuid5)

    problemId = models.CharField(max_length=10)

    language = models.CharField(max_length=20)
    version = models.CharField(max_length=10)
    source = models.TextField()

    judgeResult = models.CharField(max_length=3)
    errorLogs = models.TextField()
